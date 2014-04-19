__author__ = 'leo'


def testIt(func, *nkwargs, **kwargs):
    try:
        retval = func(*nkwargs, **kwargs)
        result = (True, retval)
    except Exception, diag:
        result = (False, str(diag))

    return result


def test():
    funcs = (int, long, float)
    vals = (123, 12.34, '1234', '12.34')
    for eachFunc in funcs:
        print '_' * 20
        for eachval in vals:
            retval = testIt(eachFunc, eachval)
            if retval[0]:
                print '%s(%s) = ' % (eachFunc.__name__, eachval), retval[1]
            else:
                print '%s(%s) = FAILED:' % (eachFunc.__name__, eachval), retval[1]

if __name__ == '__main__':
    test()