# coding=utf-8
from urllib import urlretrieve

__author__ = 'leo'


def firstNonBlank(lines):
    for eachLine in lines:
        if not eachLine.strip():
            continue
        else:
            return eachLine


def firstLast(webPage):
    f = open(webPage)
    lines = f.readlines()
    f.close()
    print firstNonBlank(lines)
    lines.reverse()
    print firstNonBlank(lines)


def download(url='http://mirror.esocc.com/apache/tomcat/tomcat-6/v6.0.36/src/apache-tomcat-6.0.36-src.tar.gz',
             process=firstLast):
    try:
        retval = urlretrieve(url, "file/asdf", cbk)[0]
    except IOError:
        retval = None
    print retval
    if retval:
        process(retval)


def cbk(a, b, c):
    '''''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' % per


if __name__ == '__main__':
    download()
