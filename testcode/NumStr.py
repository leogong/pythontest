__author__ = 'leo'
#encoding=utf8

class NumStr(object):
    def __init__(self, num=0, string=''):
        self.num = num
        #double underlines mean not directly accessible(really is "_NumStr__num")
        self.__num = num
        self.__string = string

    def __str__(self):
        return '[%d :: %r]' % (self.__num, self.__string)

    __repr__ = __str__

    def __add__(self, other):
        if isinstance(other, NumStr):
            return self.__class__(self.__num + other.__num, self.__string + other.__string)
        else:
            raise TypeError, "Illegal argument type for built-in operation"

    def __mul__(self, num):
        if isinstance(num, int):
            return self.__class__(self.__num * num, self.__string * num)
        else:
            raise TypeError, "Illegal argument type for built-in operation"

    def __nonzero__(self):
        return self.__num or len(self.__string)

    def __norm_cval(self, cmpres):
        return cmp(cmpres, 0)

    def __cmp__(self, other):
        return self.__norm_cval(cmp(self.__num, other.__num)) + self.__norm_cval(cmp(self.__string, other.__string))


a = NumStr(string='aa')

print a._NumStr__num