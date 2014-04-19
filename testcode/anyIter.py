__author__ = 'leo'


class AnyIter(object):
    def __init__(self, data, safe=False):
        self.safe = safe
        self.iter = iter(data)

    def __iter__(self):
        return self

    def next(self, howMany=1):
        retVal = []
        for eachItem in range(howMany):
            try:
                retVal.append(self.iter.next())
            except:
                if self.safe:
                    break
                else:
                    raise
        return retVal
