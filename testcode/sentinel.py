#encoding=utf-8

import Queue
import sys
from threading import Thread
import urllib
import os
import time
import socket
import thread

#【可配置】程序启动时，显示的簇点列表
apis = ('coronet.api.total.calls', 'ui.dynative', 'tmallSearch.searchItems', 'tmallSearch.searchShops', 'tmallDetail.query', 'item.info', 'rate.getRates', 'tmallCart.queryCartList', 'tmallOrder.query', 'tmallOrder.create')

#【可配置】使用排序功能时，显示的簇点个数
num = 30

#【可配置】刷新时间
refreshTime = 5

#【可配置】主机列表文件,请使用绝对路径
hostfilename = "/home/long.huangxl/coronethost"

# 【可配置】感兴趣的簇点列表，当使用排序输出功能时，只显示列表中的簇点
resources = ("coronet.api.total.calls","activity.getActivityItemList", "aladdin.cast", "aladdin.guessLike", "aladdin.myStreetIndex", "aladdin.myStreetItems", "aladdin.recommendItems", "alipayQRCode.scan", "auth.permissions", "auth.queryPrompt", "auth.requestAuth", "banner.activeList", "banner.getBannerList", "brands.getBrandById", "brands.getBrandByKey", "brands.getBrands", "brands.isCollect", "brands.list", "brands.update", "cartshare.createInitiativeFeed", "cartshare.getInitiativeTimeline", "cartshare.getShareItems", "cartshare.getTimeline", "cartshare.getUnreadFollowerCount", "cartshare.getUserInfo", "cartshare.likeFeed", "cartshare.switch", "cartshare.syncContacts", "comment.entrances", "comment.rate", "comment.render", "comment.subEntrance", "comment.uploadPic", "coupon.applyCoupon", "coupon.applyCouponAdv", "coupon.getCoupons", "customize.fetchMyTmallAsset", "customize.fetchMyTools", "discount.createGroup", "discount.destroyGroup", "discount.draw", "discount.groupInfo", "discount.joinGroup", "discount.leaveGroup", "dynative.mobilePromotion", "dynative.shopRecommend", "feed.categoryList", "feed.checkFollow", "feed.detail", "feed.follow", "feed.followee", "feed.followeeList", "feed.followeeListInCategory", "feed.list", "feed.unfollow", "fm.brand", "fm.category", "fm.channelItem", "fm.channelTheme", "fm.findDetail", "fm.hotTheme", "fm.index", "fm.theme", "followee.feed", "followee.outline", "hybrid.fly", "IdcFacade.invokeMethod", "item.info", "like.add", "like.del", "like.islike", "like.itemlikecnt", "like.list", "like.rank", "like.shoplikecnt", "like.synchronize", "like.update", "momBaby.babyInfo", "myStreet.brandSubject", "myStreetService.getCardList", "myStreetService.getDetail", "myStreetService.getFollowRelation", "myStreetService.getShopListVO", "myStreetService.getShops", "myStreetService.receiveCoupon", "myStreetService.unlike", "myStreetService.updateFollow", "myStreet.subjectDetail", "order.check", "order.create", "order.query", "oss.ad", "oss.brand", "oss.clientConfig", "oss.config", "oss.egg", "oss.intlBrands", "oss.itemCategory", "oss.qrCenter", "oss.queryChaoshiStore", "oss.tmsContent", "oss.ver", "postit.fetchTopic", "push.categories", "push.collect", "push.list", "push.remove", "push.reply", "push.snap", "queryOrder.periodicOrders", "queryOrder.queryOrderCount", "rate.dsrInfo", "rate.enable", "rate.getRates", "rate.getTags", "rate.submit", "rate.subOrderList", "recommend.getList", "security.tms", "shopAuctionSearch.getShopItemList", "shop.getShopInfoByDomain", "shop.info", "showcase.showcaseList", "showOffLabel.addLabel", "showOffLabel.fetchGenericLabels", "showOffLabel.fetchLabelByLabelId", "showOffLabel.fetchLabelShare", "showOffLabel.fetchMyLabels", "showOffLabel.hint", "showOffLabel.pinLabel", "showOffLabel.search", "showOffLabel.unpinLabel", "showOffMisc.getBuyerRecentItems", "showOffPost.fetchPostShare", "showOffPost.getAllReplyReportReasons", "showOffPost.getAllReportReasons", "showOffPost.getGenericPosts", "showOffPost.getHotPostsByLabel", "showOffPost.getNewPostContext", "showOffPost.getNewPostPrompt", "showOffPost.getPost", "showOffPost.getPostsByAuthor", "showOffPost.getPostsByLabel", "showOffPost.getPostsLikedBy", "showOffPost.getReplies", "showOffPost.like", "showOffPost.logSharing", "showOffPost.post", "showOffPost.reply", "showOffPost.report", "showOffPost.unlike", "showOffPost.updateImageWithLabels", "showOffUser.editProfile", "showOffUser.fetchFollowers", "showOffUser.fetchFollowings", "showOffUser.fetchLikers", "showOffUser.fetchProfile", "showOffUser.follow", "showOffUser.searchUser", "showOffUser.unfollow", "showOffUser.updateTriedEditProfile", "splash.current", "stats.report", "stats.trace", "suggestService.history", "tgh.detail", "timeline.getFilters", "timeline.getList", "tmallCard.getUserCardBlance", "tmallCart.addCart", "tmallCart.delCart", "tmallCart.queryCartList", "tmallCart.updateCartCount", "tmallDetail.locate", "tmallDetail.progressive", "tmallDetail.query", "tmallOrder.create", "tmallOrder.query", "tmallPoint.giftPoints", "tmallPoint.list", "tmallSearch.searchItems", "tmallSearch.searchShops", "topDiscount.getData", "tube.rBxt", "twShop.shopDetail", "ui.dynative", "ui.getLibs", "ui.getMenuState", "ui.getPage", "user.info", "user.member", "user.point")

iput = 0

class Worker(Thread):
    worker_count = 0

    def __init__(self, workQueue, resultQueue, timeout=0, **kwds):
        Thread.__init__(self, **kwds)
        self.id = Worker.worker_count
        Worker.worker_count += 1
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.timeout = timeout
        self.start()

    def run(self):
        while True:
            try:
                callable, args, kwds = self.workQueue.get(timeout=self.timeout)
                res = callable(*args, **kwds)
                self.resultQueue.put(res)
            except:
                pass

class WorkerManager:

    def __init__(self, num_of_workers=10, timeout=1):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self.num = num_of_workers
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue, self.timeout)
            self.workers.append(worker)

    def wait_for_complete(self):
        # ...then, wait for each of them to terminate:
        while self.resultQueue.qsize() != self.num:
            pass

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)

#handle the result of each machine
def handle(data):
    datalines = data.splitlines()
    result = {}
    for dataline in datalines:
      if len(dataline) != 0:
        dataline = dataline[dataline.rfind('-') + 1:]
        name = dataline[:dataline.find('(')]
        content = dataline[dataline.find('(')+1:dataline.rfind(')')]
        items = content.split()
        numbers = []
        for item in items:
            its = item.split(':')
            if len(its) == 2:
                numbers.append(int(its[1]))
        if len(numbers) == 8:
            result[name] = numbers
    return result

def do_job(host, sleep=0.001):
    data = ""
    try:
        data = urllib.urlopen('http://' + host + ':8719/tree').read()
    except:
        print '[%4s]' % host, sys.exc_info()[:2]
    return handle(data)

#add two map
def add(m, n):
    for key in m.keys():
        if n.has_key(key) and (key in resources):
            m[key] = listadd(m[key], n[key])
    for key in n.keys():
        if (not m.has_key(key)) and (key in resources):
            m[key] = n[key]
    return m

#add two list
def listadd(l1, l2):
    if len(l1) != 8 or len(l2) != 8:
        print 'not right'
    for i in range(len(l1)):
        l1[i] = l1[i] + l2[i]
    return l1

def inred( s ):
    return"%s[31;2m%s%s[0m"%(chr(27), s, chr(27))

def ingreen( s ):
    return"%s[32;2m%s%s[0m"%(chr(27), s, chr(27))

def now():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

#write files
files = {}

def write_data(apis, data, success):
    for api in apis:
        value = data[api]
        dd = '%-25s%15s%15s%15s%15s%15s%15s%15s%15s\n' % (now(), value[0], value[1], value[2], value[3], value[4]/success, value[5],value[6], value[7])
        files[api].write(dd)
        files[api].flush()


def handle_result(data, apis, success):
    global iput
    global num
    os.system("clear")
    write_data(apis, data, success)
    print ingreen(str(success) + "--------------------------------------------------------------------------- sentinel grail -----------------------------------------------------------------------------")
    print '%-70s%25s%25s%25s%25s%25s%25s%25s%25s' %(inred(now()), inred('thread count'), inred('pass qps'), inred('block qps'), inred('total qps'), inred('rt'), inred('1min pass'), inred('1min block'), inred('1min total'))
    datas = [(api, data[api]) for api in data.keys()]
    datass = sorted(datas, key=lambda a:a[1][iput - 1], reverse = True)
    if iput == 0:
        for api in apis:
            value = data[api]
            a = ingreen(value[0])
            b = ingreen(value[1])
            c = ingreen(value[2])
            d = ingreen(value[3])
            #average rt
            e = ingreen(value[4]/success)
            f = ingreen(value[5])
            g = ingreen(value[6])
            h = ingreen(value[7])
            print '%-70s%25s%25s%25s%25s%25s%25s%25s%25s' %(inred(api), a, b, c, d, e, f, g, h)
    else:
        for i in range(num):
            value = datass[i][1]
            api = datass[i][0]
            a = ingreen(value[0])
            b = ingreen(value[1])
            c = ingreen(value[2])
            d = ingreen(value[3])
            #average rt
            e = ingreen(value[4]/success)
            f = ingreen(value[5])
            g = ingreen(value[6])
            h = ingreen(value[7])
            print '%-70s%25s%25s%25s%25s%25s%25s%25s%25s' %(inred(api), a, b, c, d, e, f, g, h)

def openfiles(apis):
    pathname = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    os.chdir(pathname)
    for api in apis:
        files[api] = open(api, 'a')

def closefiles(apis):
    for filename in files.keys():
        files[filename].close()

def get_input():
    global last
    global apis
    global success
    global iput
    while True:
        x = input() 
        if x >= 0 and x <= 8:
            iput = x
            handle_result(last, apis, success)

def run():
    global last
    global apis
    global success
    socket.setdefaulttimeout(4)
    openfiles(apis)
    fin = open(hostfilename, 'r')
    lines = fin.readlines()
    fin.close()
    wm = WorkerManager(len(lines))
    thread.start_new_thread(get_input, ())  
    while True:
        for line in lines:
            line = line .strip()
            wm.add_job(do_job, line, 0.001)
        wm.wait_for_complete()
        data = {}
        success = wm.resultQueue.qsize()
        while wm.resultQueue.qsize():
            res = wm.resultQueue.get()
            if len(res.keys()) == 0:
                success = success - 1
            data = add(res, data)
        temp = {}
        for key in data.keys():
            if key in resources:
                temp[key] = data[key] 
        last = temp
        handle_result(temp, apis, success)
        wm.workcount = 0
        time.sleep(refreshTime)

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        closefiles(apis)
    print '\rBye bye ~'
