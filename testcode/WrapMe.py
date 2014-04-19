__author__ = 'leo'


class WrapMe(object):
    def __init__(self, obj):
        self.__data = obj

    def get(self):
        return self.__data

    def __repr__(self):
        return 'self.__data'

    def __str__(self):
        return str(self.__data)

    def __getattr__(self, item):
        return getattr(self.__data, item)


wrapperList = WrapMe([123, 'foo', 45.67])

wrapperList.append("ddd")

print getattr(wrapperList,"__str__")
