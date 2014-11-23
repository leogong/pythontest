#!/usr/bin/python# -*- coding: utf-8 -*-import urllibfrom lxml.html import soupparserfrom lxml import etreeimport reimport urllib2import timeimport sysimport MySQLdbimport chardetconn = MySQLdb.connect(host=sys.argv[1], user=sys.argv[2], passwd=sys.argv[3], db=sys.argv[4], port=3306,                       charset='utf8')cur = conn.cursor()site_url = sys.argv[6]class Recursion(Exception):    passclass Article():    title = None    page = None    categories = {}    tags = {}    def __init__(self):        passclass MyCrawler():    url = None    final_html = ""    copy_site_domain = None    my_domain = "http://%s/wp-content/uploads/%s" % (sys.argv[7]                                                     , time.strftime('%Y/%m', time.localtime(time.time())))    url_compile = re.compile(r"http://(.*?)/")    root = None    article = None    def __init__(self, url):        self.url = url        self.copy_site_domain = self.url_compile.findall(url)[0]    def get_info_from_url(self):        read = urllib2.urlopen(self.url, timeout=30).read()        self.root = soupparser.fromstring(read.decode(chardet.detect(read)["encoding"]))        self.article = Article()    def replace_pre_code(self):        p = re.compile(r'<pre.*?brush:(.*?);.*?>([\s\S]*?)</pre>')        def func(m):            return '[' + m.group(1).strip() + ']' + m.group(2) + '[/' + m.group(1).strip() + ']'        self.final_html = p.sub(func, self.final_html)    @staticmethod    def filter_content(html_code):        if "感谢" in html_code or "原文链接" in html_code:            return True    @staticmethod    def filter_ending(html_code):        if "（全文完）" in html_code:            return True    def replace_img(self, html_code):        img_list = html_code.findall('.//img')        for img_tag in img_list:            img_src = img_tag.get("src")            new_image_url = self.my_domain + img_src[img_src.rindex("/"):]            img_tag.set('src', new_image_url)    def is_adaptive(self, url):        if url:            compile_findall = self.url_compile.findall(url)            if len(compile_findall) and compile_findall[0] != self.copy_site_domain:                return True    def replace_url(self, html_code):        a_tag_list = html_code.findall('.//a')        for a_tag in a_tag_list:            is_img_url = False            url_href = a_tag.get('href')            if a_tag is not None:                child_img = a_tag.find('img')                if child_img is not None:                    img_src = child_img.get('src')                    if img_src[img_src.rindex("/"):] == url_href[url_href.rindex("/"):]:                        a_tag.set('href', img_src)                        is_img_url = True            if not is_img_url and self.is_adaptive(url_href):                # todo return article url                my_craw = MyCrawler("http://coolshell.cn/articles/12012.html")                article = my_craw.start()                DbHandler.save_article(article)                pass    def get_article_content(self):        article_sub_element = self.root.find('.//div[@class="post"]/div[@class="content"]')        for sub_element in article_sub_element:            piece_of_html = etree.tostring(sub_element, encoding="utf-8", method="html")            if self.filter_content(piece_of_html):                continue            if self.filter_ending(piece_of_html):                break            self.replace_img(sub_element)            self.replace_url(sub_element)            self.final_html += etree.tostring(sub_element, encoding="utf-8", method="html")            self.replace_pre_code()            self.article.page = self.final_html    def get_categories(self):        categories = self.root.xpath('.//div[@class="under"]/span[2]/a')        for category in categories:            r_index__strip = self.get_value_from_url(category.get('href'))            self.article.categories[r_index__strip] = category.text.encode("utf-8").strip()    def get_tags(self):        tags = self.root.xpath('.//div[@class="under"]/span[4]/a')        for tag in tags:            r_index__strip = self.get_value_from_url(tag.get('href'))            self.article.tags[r_index__strip] = tag.text.encode("utf-8").strip()    @staticmethod    def get_value_from_url(url):        value = url[url.rindex("/") + 1:]        if not value:            value = url[url.rindex("/", 0, len(url) - 1) + 1:]        return value.strip()    def start(self):        self.get_info_from_url()        self.get_article_content()        # todo get keyword description        self.get_categories()        self.get_tags()        self.get_title()        return self.article    def get_title(self):        title = self.root.xpath(".//title")[0].text.encode("utf-8").strip()        self.article.title = title[:title.index("|")]class DbHandler():    def __init__(self):        pass    @staticmethod    def save_article(article):        if article:            cur.execute("select ID from wp_users where user_login = %s", (sys.argv[5],))            user = cur.fetchone()            if not user:                raise Recursion("user not exists,user:%s" % sys.argv[5])            user_id = user[0]            cur.execute(                "INSERT INTO wp_posts(post_author, post_date, post_date_gmt, post_content, "                "post_title, post_excerpt, post_status,comment_status, ping_status, "                "post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt, "                "post_content_filtered, post_parent, guid, menu_order, post_type, post_mime_type, comment_count) "                "VALUES (%s, now(), now(), %s, %s, '', 'publish', 'open', 'open', '', "                "%s, '', '', now(), now(), '', 0, '', 0, 'post', '', 0)",                (user_id, article.page, article.title, urllib.quote(article.title)))            article_id = cur.lastrowid            cur.execute('update wp_posts set guid = %s where ID = %s',                        ("http://" + site_url + "/?p=" + str(article_id), article_id))            for slug, description in article.tags.items():                DbHandler.save_terms(article_id, slug, description)            for slug, description in article.categories.items():                DbHandler.save_terms(article_id, slug, description, True)            return "http://%s/%s.html" % (site_url, article_id)    @staticmethod    def save_terms(article_id, slug, description, is_tag=False):        description = urllib.unquote(description)        taxonomy = "post_tag" if is_tag else "category"        cur.execute(            "select wtt.term_taxonomy_id from wp_terms wt inner join wp_term_taxonomy wtt "            "on wt.term_id = wtt.term_id where wt.slug = %s and wtt.taxonomy = %s", (slug, taxonomy))        wp_terms = cur.fetchone()        if wp_terms is not None:            term_taxonomy_id = wp_terms[0]            cur.execute("update wp_term_taxonomy set count = count+1 where term_taxonomy_id = %s", (term_taxonomy_id,))        else:            cur.execute("INSERT INTO wp_terms(name,slug,term_group) VALUES (%s,%s,%s)",                        (description, slug, 0))            cur.execute(                "insert into wp_term_taxonomy(term_id,taxonomy,description,parent,count) values (%s,%s,%s,%s,%s)",                (cur.lastrowid, taxonomy, description, 0, 1))            term_taxonomy_id = cur.lastrowid        cur.execute("insert into wp_term_relationships values (%s,%s,%s)", (article_id, term_taxonomy_id, 0))try:    my_craw = MyCrawler("http://coolshell.cn/articles/12012.html")    article = my_craw.start()    DbHandler.save_article(article)    conn.commit()except Exception, e:    conn.rollback()    print e