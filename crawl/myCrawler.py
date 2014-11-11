#!/usr/bin/python# -*- coding: utf-8 -*-import urllibfrom lxml.html import soupparserfrom lxml import etreeimport reimport urllib2import timeimport sysimport chardetclass Recursion(Exception):    passclass MyCrawler():    url = None    final_html = ""    copy_site_domain = None    my_domain = "http://%s/wp-content/uploads/%s" % (sys.argv[1], time.strftime('%Y/%m', time.localtime(time.time())))    url_compile = re.compile(r"http://(.*?)/")    root = None    categories = {}    tags = []    def __init__(self, url):        self.url = url        self.copy_site_domain = self.url_compile.findall(url)[0]    def get_info_from_url(self):        read = urllib2.urlopen(self.url).read()        self.root = soupparser.fromstring(read.decode(chardet.detect(read)["encoding"]))    def replace_pre_code(self):        p = re.compile(r'<pre.*?brush:(.*?);.*?>([\s\S]*?)</pre>')        def func(m):            return '[' + m.group(1).strip() + ']' + m.group(2) + '[/' + m.group(1).strip() + ']'        self.final_html = p.sub(func, self.final_html)    @staticmethod    def filter_content(html_code):        if "感谢" in html_code or "原文链接" in html_code:            return True    @staticmethod    def filter_ending(html_code):        if "（全文完）" in html_code:            return True    def replace_img(self, html_code):        img_list = html_code.findall('.//img')        for img_tag in img_list:            img_src = img_tag.get("src")            new_image_url = self.my_domain + img_src[img_src.rindex("/"):]            img_tag.set('src', new_image_url)    def is_adaptive(self, url):        if url:            compile_findall = self.url_compile.findall(url)            if len(compile_findall) and compile_findall[0] != self.copy_site_domain:                return True    def replace_url(self, html_code):        a_tag_list = html_code.findall('.//a')        for a_tag in a_tag_list:            is_img_url = False            url_href = a_tag.get('href')            if a_tag is not None:                child_img = a_tag.find('img')                if child_img is not None:                    img_src = child_img.get('src')                    if img_src[img_src.rindex("/"):] == url_href[url_href.rindex("/"):]:                        a_tag.set('href', img_src)                        is_img_url = True            if not is_img_url and self.is_adaptive(url_href):                # todo return article url                # my_craw = MyCrawler(url_href)                # my_craw.start()                pass    def get_article_content(self):        article_sub_element = self.root.find(u'.//div[@class="post"]/div[@class="content"]')        for sub_element in article_sub_element:            piece_of_html = etree.tostring(sub_element, encoding="utf-8", method="html")            if self.filter_content(piece_of_html):                continue            if self.filter_ending(piece_of_html):                break            self.replace_img(sub_element)            self.replace_url(sub_element)            self.final_html += etree.tostring(sub_element, encoding="utf-8", method="html")            self.replace_pre_code()    def get_categories(self):        categories = self.root.xpath('.//div[@class="under"]/span[2]/a')        for category in categories:            category_url = urllib.unquote(category.attrib['href'])            r_index__strip = category_url[category_url.rindex("/") + 1:].strip()            self.categories[r_index__strip] = category.text.encode("utf-8").strip()    def get_tags(self):        tags = self.root.xpath('.//div[@class="under"]/span[4]/a')        for tag in tags:            self.tags.append(tag.text.encode("utf-8").strip())    def start(self):        self.get_info_from_url()        self.get_article_content()        self.get_categories()        self.get_tags()my_craw = MyCrawler("http://coolshell.cn/articles/11973.html")my_craw.start()print my_craw.final_html