__author__ = 'leo'

aDict = {}
aFile = open("aaa", 'r')
fileLines = aFile.readlines()
for oneLine in fileLines:
    line_split = oneLine.split("\t")
    seq = line_split[0]
    wrapper = line_split[1]
    wrapper = wrapper
    wrapper = wrapper[:len(wrapper) - 1]
    if seq in aDict:
        list1 = list(aDict[seq])
        list1.append(wrapper)
    else:
        list1 = [wrapper]
        aDict[seq] = list1

