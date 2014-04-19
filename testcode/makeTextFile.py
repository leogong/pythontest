__author__ = 'leo'
"""makeTextFile.py -- create text file"""
import os

ls = os.linesep
while True:
    fName = raw_input("Enter fileName:")
    if os.path.exists(fName):
        print "ERROR:'%s' already exists " % fName
    else:
        break
all = []
print "\nEnter lines ('.' by itself to quit).\n"

while True:
    entry = raw_input('> ')
    if entry == '.':
        break
    else:
        all.append(entry)
fobj = open(fName, 'w')
print ls
print ['%s%s' % (x, ls) for x in all]
fobj.writelines(['%s%s' % (x, ls) for x in all])
fobj.close()
print 'Done!'

