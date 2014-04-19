__author__ = 'leo'


class InstCt(object):
    count = 0

    def __init__(self):
        InstCt.count += 1
        print "init count:%s" % InstCt.count

    def __del__(self):
        InstCt.count -= 1
        print "del count:%s" % InstCt.count

    def howMany(self):
        return InstCt.count


a = InstCt()
b = InstCt()

print InstCt.count

print "a.howMany : %s" % a.howMany()
print "b.howMany : %s" % b.howMany()

del b

print "a.howMany : %s" % a.howMany()

