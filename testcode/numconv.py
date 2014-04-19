__author__ = 'leo'


def convert(func, seq):
    return [func(eachNum) for eachNum in seq]


myseq = (123, 46.67, -6.2e8, 999999999999L)

print convert(int, myseq)
print convert(long, myseq)
print convert(float, myseq)

