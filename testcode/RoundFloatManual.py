__author__ = 'leo'


class RoundFloatManual(object):
    def __init__(self, val):
        assert isinstance(val, float), "Value must be a float"
        self.value = val

    def __str__(self):
        return str("value = %s " % self.value)

    __repr__ = __str__


c = RoundFloatManual(10.0)

print c.__str__
print RoundFloatManual.__str__