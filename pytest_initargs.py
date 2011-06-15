from _pytest import python
import inspect

def pytest_pycollect_makeitem(collector, name, obj):
    if inspect.isclass(obj):
        if collector.classnamefilter(name):
            if python.hasinit(obj) and hasattr(obj, 'pytest_initargs'):
                return ClassWithInit(name, parent=collector)

class ClassWithInit(python.Class):

    def collect(self):
        items = []
        for initargs in self.obj.pytest_initargs:
            arglist = map(repr, initargs.args)
            kwlist = ['%s = %r' % (name, value)
                      for name, value in initargs.kwargs.iteritems()]
            name = '(%s)' % ', '.join(arglist + kwlist)
            item = InstanceWithInit(name=name, parent=self, initargs=initargs)
            items.append(item)
        return items

class InstanceWithInit(python.Instance):

    def __init__(self, initargs, **kwds):
        python.Instance.__init__(self, **kwds)
        self.initargs = initargs

    def _getobj(self):
        args = self.initargs.args
        kwargs = self.initargs.kwargs
        return self.parent.obj(*args, **kwargs)
