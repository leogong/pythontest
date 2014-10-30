# coding=utf-8
__author__ = 'leo'

'''
Created on 2010-9-15

'''

import urllib2
import re
import socket


DEBUG = 0

'''
工具类
'''


class Tools():
    # log函数
    def __init__(self):
        pass

    @staticmethod
    def write_log(level, info):
        if DEBUG == 0:
            try:
                print "[" + level + "]" + info.decode('UTF-8').encode('GBK')
            except Exception, e:
                print "[" + level + "]" + info.encode('GBK')
                print e
        else:
            print "[" + level + "]" + info
            # if notify:
            # print "[notify]报告管理员!!"

    # 转unicode
    @staticmethod
    def to_unicode(s, charset):
        if charset == "":
            return s
        else:
            try:
                u = unicode(s, charset)
            except Exception, e:
                u = ""
                print e
        return u

        # 正则抓取

    # @param single 是否只抓取一个
    @staticmethod
    def get_from_patten(patten, src, single=False):
        rst = ""
        p = re.compile(patten, re.S)
        all_result = p.findall(src)
        for matcher in all_result:
            rst += matcher + " "
            if single:
                break
        return rst.strip()


'''
网页内容爬虫
'''


class PageGripper():
    URL_OPEN_TIMEOUT = 10  # 网页超时时间
    MAX_RETRY = 3  # 最大重试次数

    def __init__(self):
        socket.setdefaulttimeout(self.URL_OPEN_TIMEOUT)

    # 获取字符集
    @staticmethod
    def get_charset(s):
        rst = Tools.get_from_patten(u'charset=(.*?)"', s, True)
        if rst != "":
            if rst == "utf8":
                rst = "utf-8"
        return rst

    # 尝试获取页面
    def download_url(self, url_str):
        charset = ""
        page = ""
        retry = 0
        while True:
            try:
                fp = urllib2.urlopen(url_str)
                while True:
                    line = fp.readline()
                    if charset == "":
                        charset = self.get_charset(line)
                    if not line:
                        break
                    page += Tools.to_unicode(line, charset)
                    fp.close()
                    return page
                break
            except urllib2.HTTPError, e:  # 状态错误
                Tools.write_log('error', 'HTTP状态错误 code=' + e.code)
                raise urllib2.HTTPError
            except urllib2.URLError, e:  # 网络错误超时
                print e
                Tools.write_log('warn', '页面访问超时,重试..')
                retry += 1
                if retry > self.MAX_RETRY:
                    Tools.write_log('warn', '超过最大重试次数,放弃')
                    raise urllib2.URLError

    # 获取页面
    def get_page_info(self, url_str):
        Tools.write_log("info", "开始抓取网页,url= " + url_str)
        try:
            info = self.download_url(url_str)
        except:
            raise
        Tools.write_log("debug", "网页抓取成功")
        return info


'''
内容提取类
'''


class InfoGripper():
    pageGripper = PageGripper()

    def __init__(self):
        Tools.write_log('debug', "爬虫启动")

    # 抓取标题
    def grip_title(data):
        title = Tools.get_from_patten(u'box2t sp"><h3>(.*?)</h3>', data, True)
        if title == "":
            title = Tools.get_from_patten(u'<title>(.*?)[-<]', data, True)
        return title.strip()

    # 抓取频道
    def grip_channel(self, data):
        zone = Tools.get_from_patten(u'频道：(.*?)</span>', data, True)
        channel = Tools.get_from_patten(u'<a.*?>(.*?)</a>', zone, True)
        return channel

    # 抓取标签
    @staticmethod
    def grip_tag(data):
        zone = Tools.get_from_patten(u'标签：(.*?)</[^a].*>', data, True)
        rst = Tools.get_from_patten(u'>(.*?)</a>', zone, False)
        return rst

    # 抓取观看次数
    @staticmethod
    def grip_views(data):
        rst = Tools.get_from_patten(u'已经有<em class="hot" id="viewcount">(.*?)</em>次观看', data)
        return rst

    # 抓取发布时间
    @staticmethod
    def grip_time(data):
        rst = Tools.get_from_patten(u'在<em>(.*?)</em>发布', data, True)
        return rst

    # 抓取发布者
    @staticmethod
    def grip_user(data):
        rst = Tools.get_from_patten(u'title="点击进入(.*?)的用户空间"', data, True)
        return rst

    # 获取页面字符集
    @staticmethod
    def get_page_charset(data):
        charset = Tools.get_from_patten(u'charset=(.*?)"', data, True)

        if charset == "utf8":
            charset = "utf-8"
        return charset

    # 获取CC相关数据
    @staticmethod
    def get_cc_data(data):

        zone = Tools.get_from_patten(u'SWFObject(.*?)</script>', data, True)

        # 判断是否使用bokecc播放
        is_from_boke_cc = re.match('.*bokecc.com.*', zone)
        if not is_from_boke_cc:
            return "", ""

        ccSiteId = Tools.get_from_patten(u'siteid=(.*?)[&,"]', zone, True)
        ccVid = Tools.get_from_patten(u'vid=(.*?)[&,"]', zone, True)
        return ccSiteId, ccVid

    # 获取站内vid
    @staticmethod
    def grip_video_id(data):
        vid = Tools.get_from_patten(u'var vid = "(.*?)"', data, True)
        return vid

    # 获取点击量
    def grip_views_ajax(self, vid, url, basedir):
        host = Tools.get_from_patten(u'http://(.*?)/', url, True)
        ajaxAddr = "http://" + host + basedir + "/index.php/ajax/video_statistic/" + vid
        '''
        try:
            content = self.pageGripper.getPageInfo(ajaxAddr)
        except Exception,e:
            print e
            Tools.write_log ("error", ajaxAddr+u"抓取失败")
            return "error"
        '''
        Tools.write_log('debug', u"开始获取点击量,url=" + ajaxAddr)
        retry = 0
        while True:
            try:
                fp = urllib2.urlopen(ajaxAddr)
                content = fp.read()
                fp.close()
                views = Tools.get_from_patten(u'"viewcount":(.*?),', content, True)
                views = views.replace('"', '')
                return views
            except urllib2.HTTPError, e:  # 状态错误
                Tools.write_log('error', 'HTTP状态错误 code=' + "%d" % e.code)
                return ""
            except urllib2.URLError, e:  # 网络错误超时
                print e
                Tools.write_log('warn', '页面访问超时,重试..')
                retry += 1
                if retry > self.MAX_RETRY:
                    Tools.write_log('warn', '超过最大重试次数,放弃')
                    break


    # 从网页内容中爬取点击量
    @staticmethod
    def gripViewsFromData(data):
        views = Tools.get_from_patten(u'已经有<.*?>(.*?)<.*?>次观看', data, True)
        return views

    def gripBaseDir(self, data):
        dir = Tools.get_from_patten(u"base_dir = '(.*?)'", data, True)
        return dir

    # 抓取数据
    def gripinfo(self, url_str):

        try:
            data = self.pageGripper.get_page_info(url_str)
        except:
            Tools.write_log("error", url_str + " 抓取失败")
            raise

        Tools.write_log('info', '开始内容匹配')
        rst = {}
        rst['title'] = self.grip_title(data)
        rst['channel'] = self.grip_channel(data)
        rst['tag'] = self.grip_tag(data)
        rst['release'] = self.grip_time(data)
        rst['user'] = self.grip_user(data)
        ccdata = self.get_cc_data(data)
        rst['ccsiteId'] = ccdata[0]
        rst['ccVid'] = ccdata[1]
        views = self.gripViewsFromData(data)
        if views == "" or not views:
            vid = self.grip_video_id(data)
            basedir = self.gripBaseDir(data)
            views = self.grip_views_ajax(vid, url_str, basedir)
            if views == "":
                views = "error"
            if views == "error":
                Tools.write_log("error", "获取观看次数失败")
        Tools.write_log("debug", "点击量:" + views)
        rst['views'] = views
        Tools.write_log('debug', 'title=%s,channel=%s,tag=%s' % (rst['title'], rst['channel'], rst['tag']))
        return rst


'''
单元测试
'''
if __name__ == '__main__':
    list = [
        'http://008yx.com/xbsp/index.php/video/index/3138',
        'http://vblog.xwhb.com/index.php/video/index/4067',
        'http://demo.ccvms.bokecc.com/index.php/video/index/3968',
        'http://vlog.cnhubei.com/wuhan/20100912_56145.html',
        'http://vlog.cnhubei.com/html/js/30271.html',
        'http://www.ddvtv.com/index.php/video/index/15',
        'http://boke.2500sz.com/index.php/video/index/60605',
        'http://video.zgkqw.com/index.php/video/index/334',
        'http://yule.hitmv.com/html/joke/27041.html',
        'http://www.ddvtv.com/index.php/video/index/11',
        'http://www.zgnyyy.com/index.php/video/index/700',
        'http://www.kdianshi.com/index.php/video/index/5330',
        'http://www.aoyatv.com/index.php/video/index/127',
        'http://v.ourracing.com/html/channel2/64.html',
        'http://v.zheye.net/index.php/video/index/93',
        'http://vblog.thmz.com/index.php/video/index/7616',
        'http://kdianshi.com/index.php/video/index/5330',
        'http://tv.seeyoueveryday.com/index.php/video/index/95146',
        'http://sp.zgyangzhi.com/html/ji/2.html',
        'http://www.xjapan.cc/index.php/video/index/146',
        'http://www.jojy.cn/vod/index.php/video/index/399',
        'http://v.cyzone.cn/index.php/video/index/99',
    ]

    list1 = ['http://192.168.25.7:8079/vinfoant/versionasdfdf']

    infoGripper = InfoGripper()
    for url in list:
        infoGripper.gripinfo(url)
    del infoGripper