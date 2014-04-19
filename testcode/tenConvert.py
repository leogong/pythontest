import urllib2
#coding=utf8
__author__ = 'leo'

urlTemple = "http://www.baidu.com/s?wd="

for eachKey in open("../file/querykey", 'r'):
    eachKey = eachKey.strip()
    if eachKey != '\n':
        url = urlTemple + eachKey
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        text = response.read()
        try:
            print eachKey, text[text.index("<title>") + 7:text.index("_百度搜索")]
        except Exception, e:
            print e
            continue
