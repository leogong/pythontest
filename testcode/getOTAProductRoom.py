#coding=utf-8
# import os
# import re
from xml.dom import minidom
import urllib2
# import time



#dict={"a":"apple","b":"banana","o":"orange"}
broadband_dict = {"0": "无", "1": "有", "2": "免费", "3": "收费", "4": "部分收费", "5": "部分有且收费", "6": "部分有且免费", "7": "部分有且部分收费"}
#NONE(0, "无"), HAVE(1, "有"), FREE(2, "免费"), CHARGE(3, "收费"), PART_CHARGE(4, "部分收费"), PART_HAVE_CHARGE(5, "部分有且收费"), PART_HAVE_FREE(6,"部分有且免费"), PART_HAVE_PART_FREE(7, "部分有且部分收费")
bed_dict = {"0": "大床", "1": "双人床", "2": "大/双床", "3": "三床", "4": "一双一单", "5": "单人床", "6": "上下铺", "7": "通铺", "8": "榻榻米",
            "9": "水床", "10": "圆床", "11": "拼床"}
#BIG(0, "大床"), DOUBLE(1, "双人床"), BIG_DOUBULE(2, "大/双床"), THREE(3, "三床"), TWO_ONE(4, "一双一单"), ONE(5, "单人床"), UP_DOWN(6, "上下铺"), WIDE(7, "通铺"), TAMI(8, "榻榻米"), WATER(9, "水床"), ROUND(10, "圆床"), SPELL(11, "拼床
break_dict = {"0": "无早", "1": "含早", "2": "单早", "3": "双早", "4": "三早", "5": "四早"}
#NONE(0, "无早"), HAVE(1, "含早"), ONE(2, "单早"), TWO(3, "双早"), THREE(4, "三早"), FOUR(5, "四早");

#wrapper_id 酒店ID 酒店名 房型ID 房型名 床型 宽带 早餐

#resultfile = open("/home/hanqing.shi/ota/productroom.log" , "w")
inputfile = open("/home/leo/url.txt", "r")


def getCheckUrls(wrapper_all, wrapper_url):
    check_urls = []
    req = urllib2.Request(wrapper_all)
    response = urllib2.urlopen(req)
    text = response.read()
    doc = minidom.parseString(text)
    root = doc.documentElement
    user_nodes = root.getElementsByTagName("hotel")
    for node in user_nodes:
        hotelid = node.getAttribute("id")
        check_urls.append(replaceHotelId(wrapper_url, hotelid))
    return check_urls


def replaceHotelId(wrapper_url, id):
    if wrapper_url.find("?") > 0:
        wrapper_url = wrapper_url[0:len(wrapper_url) - 1] + "&hotelId=" + str(
            id) + "&fromDate=2013-03-28&toDate=2013-03-29"
    else:
        wrapper_url = wrapper_url[0:len(wrapper_url) - 1] + "?hotelId=" + str(
            id) + "&fromDate=2013-03-28&toDate=2013-03-29"
    return wrapper_url


def getRoomInfo(wrapper_id, wrapper_detail_url):
    req = urllib2.Request(wrapper_detail_url)
    response = urllib2.urlopen(req)
    text = response.read()
    doc = minidom.parseString(text)
    root = doc.documentElement
    hotelid = root.getAttribute("id")
    hotelname = root.getAttribute("name")
    room_nodes = root.getElementsByTagName("rooms")[0].getElementsByTagName("room")
    for room in room_nodes:
        roomid = room.getAttribute("id")
        name = room.getAttribute("name")
        breakfast = room.getAttribute("breakfast")
        bed = room.getAttribute("bed")
        broadband = room.getAttribute("broadband")
        counts = room.getAttribute("counts")
        #wrapper_id 酒店ID 酒店名 房型ID 房型名 床型 宽带 早餐 counts
        try:
            resultline = wrapper_id + "\t" + str(hotelid) + "\t" + hotelname.encode('utf-8') + "\t" + str(
                roomid) + "\t" + name.encode('utf-8') + "\t" + bed_dict[bed] + "\t" + broadband_dict[broadband] + "\t" + break_dict[breakfast] + "\t" + str(counts)
            #print wrapper_id , hotelid , hotelname.encode('utf-8') , roomid , name.encode('utf-8') , bed_dict[bed] , broadband_dict[broadband] , break_dict[breakfast]
            print resultline
        except Exception, e:
            print e
            continue


#getRoomInfo("wiotatts007" , "http://www.tripeasy.cn/api/Qroomlistxml-d6345a89ed20e38f7c131ce03b82412e.xml?hotelId=10443&fromDate=2013-03-27&toDate=2013-03-31")
#resultfile = open("/home/q/ota_performance_wrapper/conf/ota_wrapper.log" , "w")
#inputfile = open("")

for line in inputfile.readlines():
    wrapper_info = line.split("\t")
    wrapper_name = wrapper_info[0]
    wrapper_all = wrapper_info[1]
    wrapper_url = wrapper_info[2]
    #print wrapper_all , wrapper_url
    try:
        urls = getCheckUrls(wrapper_all, wrapper_url)
    except:
        continue
    for url in urls:
        #print url
        try:
            getRoomInfo(wrapper_name, url)
        except:
            continue

inputfile.close()
#resultfile.close()


