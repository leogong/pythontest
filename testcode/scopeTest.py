__author__ = 'leo'

j, k = 1, 2


def procl():
    j, k = 3, 4
    print "j==%d and k == %d" % (j, k)
    k = 5


def procl2():
    j = 6
    procl()
    print "j==%d and k = %d" % (j, k)


k = 7
procl()
print "j ==%d and k == %d" % (j, k)

j = 8
procl2()
print "j==%d and k ==%d" % (j, k)

