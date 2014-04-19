from random import randint, choice, randrange
from string import lowercase
from sys import maxint

__author__ = 'leo'

doms = ('com', 'edu', 'net', 'org', 'gov')

for i in range(randint(5, 10)):
    dtint = randint(0, maxint - 1)
    #dtstr = ctime(dtint)
    dtstr = randrange(2 ** 32)
    shorter = randint(4, 7)

    em = ''

    for j in range(shorter):
        em += choice(lowercase)

    longer = randint(shorter, 12)
    dn = ''
    for j in range(longer):
        dn += choice(lowercase)
    print "%s::%s@%s.%s::%d-%d-%d" % (dtstr, em, dn, choice(doms), dtint, shorter, longer)
