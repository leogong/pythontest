import pickle

__author__ = 'leo'


class FileDescribe(object):
    saved = []

    def __init__(self, name=None):
        self.name = name

    def __get__(self, obj, type1=None):
        if self.name not in FileDescribe.saved:
            raise AttributeError, "%r used before assignment" % self.name
        try:
            f = open(self.name, 'r')
            val = pickle.load(f)
            f.close()
            return val

        except(pickle.UnpicklingError, IOError, EOFError, ImportError, IndexError), e:
            raise AttributeError, "could not read %r: %s" % self.name


    def __set__(self, obj, val):
        f = open(self.name, 'w')
        try:
            pickle.dump(val, f)
            FileDescribe.saved.append(self.name)
        except (TypeError, pickle.PicklingError), e:
            raise AttributeError, "could not pickle %r" % self.name

        finally:
            f.close()

            # def __delete__(self, instance):
            #     try:
            #         os.unlink(self.name)
            #         FileDescribe.saved.remove(self.name)
            #     except (OSError, ValueError), e:
            #         pass


a = FileDescribe("name")

a.foo = 1
a.boo = 2

print a.foo, a.boo

print FileDescribe.saved
print FileDescribe.saved
print FileDescribe.saved