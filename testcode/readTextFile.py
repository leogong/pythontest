__author__ = 'leo'

fName = raw_input("Enter fileName: ")
print

try:
    fobj = open(fName, "r")
except IOError, e:
    print "*** file opern error :", e
else:
    for eachLine in fobj:
        print eachLine,
    fobj.close()
