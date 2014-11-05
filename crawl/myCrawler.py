#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml.html import soupparser
from lxml import etree
import re
import urllib2
import time


class MyCrawler():
    url = None
    html_content = None
    valuable = None
    article_content = None
    final_html = ""
    copy_site_domain = None
    my_domain = "http://static.javacode.cn/wp-content/uploads/" + time.strftime('%Y/%m', time.localtime(time.time()))


    def __init__(self, url):
        self.url = url
        re_search = re.search(r"http://(.*?)/", url)
        self.copy_site_domain = re_search.group(1)

    def get_info_from_url(self):

        self.html_content = urllib2.urlopen(self.url).read()

    def replace_pre_code(self):
        p = re.compile(r'<pre.*?brush:(.*?);.*?>([\s\S]*?)</pre>')

        def func(m):
            return '[' + m.group(1).strip() + ']' + m.group(2) + '[/' + m.group(1).strip() + ']'

        return p.sub(func, self.html_content)

    def get_article_content(self):
        root = soupparser.fromstring(self.html_content)
        article_sub_element = root.find('.//div[@class="post"]/div[@class="content"]')
        # remote letter of thanks
        if "感谢" in etree.tostring(article_sub_element[0], encoding="utf-8"):
            article_sub_element = article_sub_element[1:len(article_sub_element) - 1]
        for sub_element in article_sub_element:
            if "（全文完）" in etree.tostring(sub_element, encoding="utf-8", method="html", pretty_print=True):
                break
            img_list = sub_element.findall('.//img')
            if img_list is not None:
                for img_tag in img_list:
                    img_src = img_tag.get("src")
                    new_image_url = self.my_domain + img_src[img_src.rindex("/"):]
                    img_tag.set('src', new_image_url)
                    img_parent = img_tag.getparent()
                    if img_parent is not None and img_parent.tag == 'a':
                        img_parent.set('href', new_image_url)
            a_tag_list = sub_element.findall('.//a')
            for a_tag in a_tag_list:
                if a_tag is not None:
                    child_img = a_tag.find('img')
                    if child_img is None:
                        url_href = a_tag.get('href')
                        # if url_href and self.copy_site_domain in url_href:
                        #     print url_href
            sub_element_string = etree.tostring(sub_element, encoding="utf-8", method="html", pretty_print=True)
            print sub_element_string
            self.final_html += sub_element_string
        print self.replace_pre_code()


my_craw = MyCrawler("http://coolshell.cn/articles/12012.html")
my_craw.get_info_from_url()
my_craw.get_article_content()


