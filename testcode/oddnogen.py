from random import randint

__author__ = 'leo'

allNums = []

for eachNum in range(9):
    allNums.append(randint(1, 99))
print allNums
print filter(lambda b: b % 2, allNums)

print [n for n in [randint(1, 99) for i in range(9)] if n % 2]
