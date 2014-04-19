#coding=utf-8
import MySQLdb
import cookielib
import json
import sys
from time import sleep, ctime

import mechanize


reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = 'leo'

url = sys.argv[3]
sso_login_url = sys.argv[4]
flag = True

conn = MySQLdb.connect(host='localhost', user='root', passwd='gonglin', db='mywork', port=3306, charset='utf8')
cur = conn.cursor()

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=4)
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(sso_login_url)
br.select_form(name="loginForm")
br["_fm.l._0.a"] = sys.argv[1]
br['_fm.l._0.p'] = sys.argv[2]
br.submit()


def insert_db(kargs):
    print 'insert into info(name,job_level,job_desc,start_date,is_technical,emp_id,position_category,manager) values(%s,%s,%s,%s,1,"%s",%s,"%s")' % (
        kargs['name'], kargs['job_level'], kargs['job_desc'], kargs['start_date'], kargs['emp_id'],
        kargs['position_category'], kargs.get('manager', ''))
    # db = DB('localhost', 'root', 'gonglin', 'mywork')
    cur.execute(
        'insert into info(name,job_level,job_desc,start_date,is_technical,emp_id,position_category,manager) values(%s,%s,%s,%s,1,"%s",%s,"%s")' % (
            kargs['name'], kargs['job_level'], kargs['job_desc'], kargs['start_date'], kargs['emp_id'],
            kargs['position_category'], kargs.get('manager', '')))
    # db.close()


def query_info_from_url(manager_id):
    print url % manager_id
    text = br.open(url % manager_id).read()
    return text


def convent_text_to_json(manager_id):
    json_text = query_info_from_url(manager_id)
    json_text = json.loads(json_text[16:json_text.index(");")])
    return json_text


def convent_chinese_text(text):
    return json.dumps(text, ensure_ascii=False)


def query_subordinate_from_json(json_str):
    return json_str['content']['items']['all_results']['person.d']['results']


def query_current_user_info(json_str):
    return json_str['content']['items']['all_results']['person.mydata']['results'][0]


def query_bean_info(json_str):
    bean_map = {'emp_id': json_str['emplId'],
                'job_level': convent_chinese_text(json_str['jobLevel']),
                'job_desc': convent_chinese_text(json_str['jobDesc']),
                'name': convent_chinese_text(json_str['lastName']),
                'start_date': convent_chinese_text(json_str['lastEmpDate']),
                'position_category': convent_chinese_text(json_str['positionCategory'])}
    return bean_map


def save_info_db(manager_id):
    for i in range(10):
        try:
            global flag
            print manager_id
            to_json = convent_text_to_json(manager_id)
            print convent_chinese_text(to_json)
            if to_json['success'] and to_json['httpStatus'] == '200':
                manager = query_current_user_info(to_json)
                if str(manager_id) == str(manager['emplId']):  # if current user is a manager
                    if flag:
                        insert_db(query_bean_info(manager))  # save info of current user
                    for subordinate in query_subordinate_from_json(to_json):
                        subordinate_map = query_bean_info(subordinate)
                        subordinate_map['manager'] = manager_id
                        insert_db(subordinate_map)
                        # if flag:
                        #     t1 = Thread(target=save_info_db, args=(subordinate_map['emp_id'],))  #指定目标函数，传入参数，这里参数也是元组
                        #     t1.start()
                        # else:
                        save_info_db(subordinate_map['emp_id'])
                    flag = False
            else:
                print "not equals"
        except TypeError:
            print "can not get the info from url continue "
            sleep(10)
            continue
        conn.commit()
        break


print " start at %s" % ctime()
save_info_db(129)
save_info_db('I0001')
save_info_db('7')
conn.commit()