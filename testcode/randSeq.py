from random import choice

__author__ = 'leo'


class RandSeq(object):
    def __int__(self, seq):
        self.data = seq

    def __iter__(self):
        return self

    def next(self):
        return choice(self.data)
