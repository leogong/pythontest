from time import ctime, sleep

__author__ = 'leo'

def tsfunc(func):
    def wrapperFunc():
        print '[%s] %s () called' % (ctime(),func.__name__)
        return func()

    return wrapperFunc

@tsfunc
def foo():
    pass

foo()
sleep(4)

for i in range(2):
    sleep(1)
    foo()
