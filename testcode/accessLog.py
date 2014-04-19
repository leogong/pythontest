# from __future__ import division
# coding=utf8

aDict = {}
result = {}
file_io = open("file/a", 'r')
for eachLine in file_io:
    line_split = eachLine.split("\t")
    key = line_split[0].strip()
    value = line_split[1].strip()
    value2 = line_split[2].strip()
    if key not in aDict:
        aList = [value]
        if value2:
            aList.append(value2)
        aDict[key] = aList

    else:
        aList = aDict[key]
        aList.append(value)
        if value2:
            aList.append(value2)

for aa in open("file/aa", 'r'):
    aa = aa.strip()
    if aa in aDict:
        result[aa] = aDict[aa]

a = 0
for k in sorted(result.keys()):
    s = set(list(result[k]))
    a += len(s)
    for v in s:
        print "\"" + v + "\",",
print
print a,
