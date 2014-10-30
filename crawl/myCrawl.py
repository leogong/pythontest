#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml.html import soupparser
from lxml import etree
import os
import re
import time

# rewrite_links good!


class MyCraw():
    def __init__(self):
        pass


def replace_pre_tag(pre_tag):
    if pre_tag.tag == 'pre':
        class_attr_str = pre_tag.get('class')
        match = re.search("brush:(.*?);", class_attr_str)
        if match:
            pre_tag.tag = match.group(1).strip()
            body = etree.SubElement(pre_tag, "java")
            print pre_tag.text


copy_site = 'coolshell.cn'
img_path = "/home/leo/aa"
domain = "http://static.javacode.cn/wp-content/uploads/" + time.strftime('%Y/%m', time.localtime(time.time()))
if not os.path.exists(img_path):
    os.mkdir(img_path)
html_content = ''.join(open("/home/leo/b.htm", "r").readlines())
dom = soupparser.fromstring(html_content)
article_content = dom.find('.//div[@class="post"]/div[@class="content"]')
# remote letter of thanks
if "感谢" in etree.tostring(article_content[0], encoding="utf-8"):
    article_content = article_content[1:len(article_content) - 1]
for p_tag in article_content:
    img_list = p_tag.findall('.//img')
    if img_list is not None and len(img_list):
        for img_tag in img_list:
            img_src = img_tag.get("src")
            new_image_url = domain + img_src[img_src.rindex("/"):]
            img_tag.set('src', new_image_url)
            img_parent = img_tag.getparent()
            if img_parent is not None and img_parent.tag == 'a':
                img_parent.set('href', new_image_url)
    a_tag_list = p_tag.findall('.//a')
    for a_tag in a_tag_list:
        if a_tag is not None:
            child_img = a_tag.find('img')
            if child_img is None:
                url_href = a_tag.get('href')
                if copy_site in url_href:
                    print url_href

    if p_tag.tag == 'pre':
        replace_pre_tag(p_tag)
    else:
        pre_list = p_tag.findall('.//pre')
        for pre_tag in pre_list:
            replace_pre_tag(pre_tag)



            # print etree.tostring(p_tag, encoding="utf-8",method="html",pretty_print=True)



