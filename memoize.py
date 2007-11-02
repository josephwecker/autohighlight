def memoize(fun):
    """A clever way to reduce the runtime on the Mystery HELL tests by
    half"""
    dictName = "__" + fun.__name__ + "_memoizer"
    def func_wrap(self, *rest):
        if rest not in self.__dict__[dictName]:
            self.__dict__[dictName][rest] = fun(self, *rest)
        return self.__dict__[dictName][rest]
    
    if '__init__' not in fun.im_class.__dict__:
        fun.im_class.__dict__['__init__'] = lambda *rest: None
    oldInit = fun.im_class.__dict__['__init__']

    def init_wrap(self, *rest):
        self.__dict__[dictName] = {}
        #print "Initializing %s" % dictName
        return oldInit(self, *rest)

    fun.im_class.__dict__['__init__'] = init_wrap
    fun.im_class.__dict__[fun.__name__] = func_wrap

if __name__ == "__main__":
    class testClass:
        def foo(self, string):
            print string
            return string

    memoize(testClass.foo)
    obj = testClass()
    print "->%s" % obj.foo("Hello")
    print "->%s" % obj.foo("Hello")
    print "->%s" % obj.foo("Gato")
    print "->%s" % obj.foo("Gato")
