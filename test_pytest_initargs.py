import py

pytest_plugins = ['pytester']

def test_normal_class(testdir):
    testdir.makepyfile('''
        pytest_plugins = ['initargs']

        class TestMyClass(object):
            def test_one(self):
                assert True
        ''')
    result = testdir.runpytest()
    assert result.ret == 0
    result.stdout.fnmatch_lines(['*=== 1 passed in * seconds ===*'])

def test_initargs(testdir):
    testdir.makepyfile('''
        import pytest
        pytest_plugins = ['initargs']

        class TestMyClass(object):

            pytest_initargs = [
                pytest.mark.arguments(10),
                pytest.mark.arguments(20),
            ]

            def __init__(self, param=None):
                self.param = param

            def test_one(self):
                print 'test_one', self.param
                assert self.param in (10, 20)
        ''')
    result = testdir.runpytest('-s')
    assert result.ret == 0
    result.stdout.fnmatch_lines([
            '*=== 2 passed in * seconds ===*',
            'test_one 10',
            'test_one 20',
            ])

def test_kwargs(testdir):
    testdir.makepyfile('''
        import pytest
        pytest_plugins = ['initargs']

        class TestMyClass(object):

            pytest_initargs = [
                pytest.mark.arguments(param=42),
            ]

            def __init__(self, param=None):
                self.param = param

            def test_one(self):
                assert self.param == 42
        ''')
    result = testdir.runpytest()
    assert result.ret == 0
    result.stdout.fnmatch_lines(['*=== 1 passed in * seconds ===*'])

def test_instance_names(testdir):
    testdir.makepyfile('''
        import pytest
        pytest_plugins = ['initargs']

        class TestMyClass(object):

            pytest_initargs = [
                pytest.mark.arguments(1, 2),
                pytest.mark.arguments(1, b=2),
                pytest.mark.arguments(b=2, a=1),
            ]

            def __init__(self, a=None, b=None):
                pass

            def test_one(self):
                assert False
        ''')
    result = testdir.runpytest('-rf')
    assert result.ret == 1
    result.stdout.fnmatch_lines([
            '*=== short test summary info ===*',
            'FAIL test_instance_names.py::TestMyClass::(1, 2)::test_one',
            'FAIL test_instance_names.py::TestMyClass::(1, b = 2)::test_one',
            'FAIL test_instance_names.py::TestMyClass::(a = 1, b = 2)::test_one',
            '*=== 3 failed in * seconds ===*'
            ])
