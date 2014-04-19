__author__ = 'leo'
#coding=utf8
'''
An example of reading and writing Unicode strings:Writes
a Unicode string to a file in UTF8 and reads it back in
'''

CODEC = 'utf-8'
FILE = 'unicode.txt'

hello_out = u"Hello world 我们\n"
bytes_out = hello_out.encode(CODEC)
f = open(FILE, "a")
f.write(bytes_out)
f.close()

f = open(FILE, "r")
bytes_in = f.read()
f.close()
hello_in = bytes_in.decode(CODEC)
print hello_in