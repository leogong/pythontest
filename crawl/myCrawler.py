#!/usr/bin/python# -*- coding: utf-8 -*-import cookielibimport randomimport tracebackimport urllibfrom lxml.html import soupparserfrom lxml import etreeimport reimport timeimport sysimport MySQLdbimport MySQLdb.cursorsimport chardetimport mechanizeimport qiniufrom qiniu.services.storage import uploader# 1         2       3       4          5        6# localhost dbUser password dbName   domain     urlconn = MySQLdb.connect(host=sys.argv[1], user=sys.argv[2], passwd=sys.argv[3], db=sys.argv[4], port=3306,                       charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)conn2 = MySQLdb.connect(host=sys.argv[1], user=sys.argv[2], passwd=sys.argv[3], db='site', port=3306,                        charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)cur = conn.cursor()cur2 = conn2.cursor()cur2.execute("select * from site where site = %s", (sys.argv[5],))site_info = cur2.fetchone()if site_info is None:    raise Exception("site_info not exists,%s" % sys.argv[5])site_url = site_info['site']br = mechanize.Browser()cj = cookielib.LWPCookieJar()br.set_cookiejar(cj)br.set_handle_equiv(True)br.set_handle_gzip(True)br.set_handle_redirect(False)br.set_handle_referer(True)br.set_handle_robots(False)br.set_handle_refresh(False)br.set_debug_redirects(True)# br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=4)br.addheaders = [('User-agent',                  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '                  'Chrome/39.0.2171.65 Safari/537.36')]img_prefix = "wp-content/uploads/%s" % (time.strftime('%Y/%m/%d/%H', time.localtime(time.time())))my_domain = "http://%s/%s" % (site_info['static_domain'], img_prefix)url_set = set()class Recursion(Exception):    passclass Circle(Exception):    passclass Article():    title = None    page = None    categories = {}    tags = {}    site_imitation = None    old_url = None    url = None    new_url = None    def __init__(self):        passclass MyCrawler():    url = None    count = 0    final_html = ""    copy_site_domain = None    url_compile = re.compile(r"http://([\w.]*)")    root = None    article = None    site_imitation = None    def __init__(self, url, count=0):        self.url = url        self.count = count        self.print_info(self.url)        self.article = Article()        self.copy_site_domain = self.url_compile.findall(url)[0]        cur2.execute("select * from site_imitation where site_id = %s and domain = %s ",                     (site_info['id'], self.copy_site_domain))        self.site_imitation = cur2.fetchone()        if self.site_imitation is None:            raise Recursion("site not exists," + url)        if url in url_set:            raise Circle(url + ",circle url")        url_set.add(url)    def get_info_from_url(self):        read = br.open(self.url).read()        self.root = soupparser.fromstring(read.decode(chardet.detect(read)["encoding"]))        self.article.old_url = self.url    def replace_pre_code(self):        p = re.compile(r'<pre.*?brush:(.*?);.*?>([\s\S]*?)</pre>')        def func(m):            return '[' + m.group(1).strip() + ']' + m.group(2) + '[/' + m.group(1).strip() + ']'        self.final_html = p.sub(func, self.final_html)        self.final_html = self.final_html.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").replace(            "&quot;", "\"")    @staticmethod    def filter_content(html_code):        if "感谢" in html_code or "原文链接" in html_code:            return True    @staticmethod    def filter_ending(html_code):        if "（全文完）" in html_code or "转载本站" in html_code:            # if "（全文完）" in html_code:            return True    def replace_img(self, html_code):        img_list = html_code.findall('.//img')        for img_tag in img_list:            img_src = img_tag.get("src")            index = img_src.find("?")            if index:                image_name = img_src[:index]                image_name = image_name[image_name.rindex("/") + 1:]            else:                image_name = img_src[img_src.rindex("/") + 1:]            new_image_url = my_domain + image_name            img_tag.set('src', new_image_url)            if not ImageHandler.uploader(img_src, img_prefix + image_name):                raise Recursion("image save failed!," + self.url)    def is_adaptive(self, url):        if url:            compile_findall = self.url_compile.findall(url)            if not len(compile_findall):                return False            elif compile_findall[0] == self.copy_site_domain:                return True            else:                cur2.execute("SELECT * FROM site_imitation where domain = %s", (compile_findall[0],))                return True if cur2.fetchone() is not None else False    def replace_url(self, html_code):        a_tag_list = html_code.findall('.//a')        for a_tag in a_tag_list:            is_img_url = False            url_href = a_tag.get('href')            if a_tag is not None:                child_img = a_tag.find('img')                if child_img is not None:                    img_src = child_img.get('src')                    if img_src[img_src.rindex("/"):] == url_href[url_href.rindex("/"):]:                        a_tag.set('href', img_src)                        is_img_url = True            if not is_img_url:                if self.is_adaptive(url_href):                    try:                        inner_craw = MyCrawler(url_href, self.count + 1)                        inner_article = inner_craw.start()                        a_tag.set('href', DbHandler.save_article(inner_article))                    except (mechanize.HTTPError, mechanize.URLError) as http_error:                        if isinstance(http_error, mechanize.HTTPError):                            a_tag.set('href', "http://" + site_url)                            self.print_info("url:%s,http error:%s" % (url_href, http_error.code))                        else:                            self.print_info("url:%s,else http error:%s" % (url_href, http_error.reason.args))                    except Circle:                        a_tag.set('href', "#")                        self.print_info("circle url:%s" % url_href)                else:                    # try:                    # br.open(url_href)                    # except (mechanize.HTTPError, mechanize.URLError) as e:                    # if isinstance(e, mechanize.HTTPError):                    # a_tag.set('href', "http://" + site_url)                    # print "url:%s,http error:%s" % (url_href, e.code)                    # else:                    # print "url:%s,else http error:%s" % (url_href, e.reason.args)                    pass    def get_article_content(self):        article_sub_element = self.root.xpath(self.site_imitation['content'])        if len(article_sub_element) == 1:            article_sub_element = self.root.find(self.site_imitation['content'])        else:            raise Recursion("no or duplicate content"), "url:%s,size:%s" % (self.url, len(article_sub_element))        i = 0        for sub_element in article_sub_element:            piece_of_html = etree.tostring(sub_element, encoding="utf-8", method="html")            if self.filter_content(piece_of_html):                continue            if self.filter_ending(piece_of_html):                break            self.replace_img(sub_element)            self.replace_url(sub_element)            self.final_html += etree.tostring(sub_element, encoding="utf-8", method="html")            if i == 2:                self.final_html += "<!--more-->"            self.replace_pre_code()            self.article.page = self.final_html            i += 1    def get_categories(self):        categories = self.root.xpath(self.site_imitation['categories'])        for category in categories:            r_index__strip = self.get_value_from_url(category.get('href'))            self.article.categories[r_index__strip] = category.text.encode("utf-8").strip()    def get_tags(self):        tags = self.root.xpath(self.site_imitation['tags'])        for tag in tags:            r_index__strip = self.get_value_from_url(tag.get('href'))            self.article.tags[r_index__strip] = tag.text.encode("utf-8").strip()    @staticmethod    def get_value_from_url(url):        value = url[url.rindex("/") + 1:]        if not value:            value = url[url.rindex("/", 0, len(url) - 1) + 1:]        return value.strip()    def start(self):        cur2.execute("select new_url from site_relation where old_url = %s and "                     "site_id = %s and site_imitation_id=%s",                     (self.url, site_info['id'], self.site_imitation['id']))        exist_page = cur2.fetchone()        if exist_page is not None:            self.print_info(self.url + ", repeat url")            self.article.new_url = exist_page['new_url']            return self.article        self.get_info_from_url()        self.get_article_content()        # todo get keyword description        self.get_categories()        self.get_tags()        self.get_title()        self.replace_keywords()        self.article.site_imitation = self.site_imitation        return self.article    def get_title(self):        title = self.root.xpath(".//title")[0].text.encode("utf-8").strip()        self.article.title = title[:title.index("|")]    def print_info(self, info):        print "    " * self.count + info    def replace_keywords(self):        keywords_ = self.site_imitation["keywords"].encode("utf-8").split(",")        my_site_keywords = site_info["keywords"].encode("utf-8").split(",")        for keyword in keywords_:            self.article.page = self.article.page.replace(keyword, my_site_keywords[                random.randint(0, len(my_site_keywords) - 1)])class DbHandler():    def __init__(self):        pass    @staticmethod    def save_article(article):        if article:            if article.new_url:                return article.new_url            try:                cur.execute("select ID from wp_users where user_login = %s", (site_info['user'],))                user = cur.fetchone()                if user is None:                    raise Recursion("user not exists,user:%s" % site_info['user'])                user_id = user['ID']                cur.execute(                    "INSERT INTO wp_posts(post_author, post_date, post_date_gmt, post_content, "                    "post_title, post_excerpt, post_status,comment_status, ping_status, "                    "post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt, "                    "post_content_filtered, post_parent, guid, menu_order, post_type, post_mime_type, comment_count) "                    "VALUES (%s, now(), now(), %s, %s, '', 'publish', 'open', 'open', '', "                    "%s, '', '', now(), now(), '', 0, '', 0, 'post', '', 0)",                    (user_id, article.page, article.title, urllib.quote(article.title)))                article_id = cur.lastrowid                cur.execute('update wp_posts set guid = %s where ID = %s',                            ("http://" + site_url + "/?p=" + str(article_id), article_id))                for slug, description in article.tags.items():                    DbHandler.save_terms(article_id, slug, description)                for slug, description in article.categories.items():                    DbHandler.save_terms(article_id, slug, description, True)                new_url = "http://%s/%s.html" % (site_url, article_id)                DbHandler.save_relation(new_url, article.site_imitation['id'], article.old_url)                conn.commit()                conn2.commit()                return new_url            except Exception, e:                conn.rollback()                conn2.rollback()                raise Recursion(e)    @staticmethod    def save_terms(article_id, slug, description, is_tag=False):        description = urllib.unquote(description)        taxonomy = "post_tag" if is_tag else "category"        cur.execute(            "select wtt.term_taxonomy_id from wp_terms wt inner join wp_term_taxonomy wtt "            "on wt.term_id = wtt.term_id where wt.slug = %s and wtt.taxonomy = %s", (slug, taxonomy))        wp_terms = cur.fetchone()        if wp_terms is not None:            term_taxonomy_id = wp_terms['term_taxonomy_id']            cur.execute("update wp_term_taxonomy set count = count+1 where term_taxonomy_id = %s", (term_taxonomy_id,))        else:            cur.execute("INSERT INTO wp_terms(name,slug,term_group) VALUES (%s,%s,%s)",                        (description, slug, 0))            cur.execute(                "insert into wp_term_taxonomy(term_id,taxonomy,description,parent,count) values (%s,%s,%s,%s,%s)",                (cur.lastrowid, taxonomy, description, 0, 1))            term_taxonomy_id = cur.lastrowid        cur.execute("insert into wp_term_relationships values (%s,%s,%s)", (article_id, term_taxonomy_id, 0))    @staticmethod    def save_relation(new_url, site_imitation_id, old_url):        cur2.execute("insert into site_relation(site_id, site_imitation_id, old_url, new_url) values (%s,%s,%s,%s)",                     (site_info['id'], site_imitation_id, old_url, new_url))class ImageHandler():    def __init__(self):        pass    @staticmethod    def uploader(url, key):        q = qiniu.Auth(site_info['ak'].encode("utf-8"), site_info['sk'].encode("utf-8"))        data = br.open(url).read()        token = q.upload_token(site_info["bucket_name"].encode("utf-8"))        ret, info = uploader.put_data(token, key, data)        # todo if file exists        # random.sample('zyxwvutsrqponmlkjihgfedcba0123456789',5)        if ret is not None:            return True        else:            print("error msg:" + info + "," + url)  # error message in info            return Falsetry:    # my_craw = MyCrawler("http://coolshell.cn/articles/11973.html")    my_craw = MyCrawler(sys.argv[6])    article = my_craw.start()    DbHandler.save_article(article)    conn.commit()    conn2.commit()except Exception, e:    conn.rollback()    conn2.rollback()    print e    print traceback.format_exc()