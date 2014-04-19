__author__ = 'lingong'


class TestStaticMethod:
    #@staticmethod
    def foo():
        print "class static method foo()"

    foo = staticmethod(foo)


class TestClassMethod:
    #@classmethod
    def foo(cls):
        print "class class method foo()"
        print "foo() is part of class:", cls.__name__

    foo = classmethod(foo)





