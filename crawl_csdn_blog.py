#!/usr/bin/env python
# -*- encoding: utf8 -*-
# 爬取csdn的数据
# author : wusuopubupt
# date : 2015-11-11
import re
import sys
import time
import sys
import urllib2
import Queue
import threading
import MySQLdb
from mysqlDriver import MySQL
from bs4 import BeautifulSoup

# 解决UnicodeDecodeError: ‘ascii’ codec can’t decode byte 0xe5 in position 108: ordinal not in range(128)
reload(sys)
sys.setdefaultencoding('utf8')

tablename = "csdn_blog_detail"
url = "http://blog.csdn.net/wusuopubupt/article/details/"
thread_num = 50

"""
请求html页面数据
"""
def getContent(url):
    # 伪造header
    send_headers = {
        'Referer' : 'http://www.csdn.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    }
    req = urllib2.Request(url,headers=send_headers)
    ret = urllib2.urlopen(req)
    html = ret.read()                             
    return html

class downloadThread(threading.Thread):
    """
    下载线程
    """
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
  
    def run(self):
        while True:
            thread_name = threading.currentThread().getName()
            id  = self.queue.get()
            res = crawl(url,id)
            print thread_name, res["title"]
            self.queue.task_done()

"""
获取所有博客id
"""
def getAllIds():
    blog_list_url = "http://blog.csdn.net/wusuopuBUPT/article/list/"
    max_page_num = 84
    id_list = open('data/id_list', 'awb+')
    for pn in range(1,max_page_num):
        # 本地文件
        f = open('data/list_'+str(pn)+'.html', 'awb+')
        content = f.read()
        if not content:
            content = getContent(blog_list_url+str(pn))
            f.write(content)
        if not content:
            print "http request page %d get null----" % pn
            return None
        """
        <span class="link_title">
            <a href="/wusuopubupt/article/details/45628007">
                Http长连接200万尝试及调优            
            </a>
        </span>

        """
        soup = BeautifulSoup(content,"html.parser")
        # 标题
        soup_title = soup.find_all(name="span", attrs={"class":"link_title"})
        for t in soup_title:
            link = t.a.get('href')
            id_regex = re.compile(r'details\/(\d+).*')
            id = id_regex.findall(link)[0]
            id_list.write(str(id)+'\n')
            print id
        f.close()
    id_list.close()

def parseContent(content):
    soup = BeautifulSoup(content,"html.parser")
    # 标题
    soup_title = soup.find(name="span", attrs={"class":"link_title"})
    #title = soup_title.a.string.strip()
    title = soup_title.a.get_text().strip()
    # tag, 发布时间，阅读次数
    soup_article_manage  = soup.find(name="div", attrs={"class":"article_manage"})
    soup_link_categories = soup_article_manage.find(name="span", attrs={"class":"link_categories"})
    if soup_link_categories:
        soup_link_tag = soup_link_categories.find_all(name="a")
    else :
        soup_link_tag = []
    tag = ""
    for a in soup_link_tag:
        if tag == "":
            tag = a.string.strip()
        else:
            tag = tag + "$$" + a.string.strip()
    post_date = soup_article_manage.find(name="span", attrs={"class":"link_postdate"}).string.strip()
    # eg: 1008人阅读
    link_view = soup_article_manage.find(name="span", attrs={"class":"link_view"}).string.strip()
    view_num_regex = re.compile(r'.*(\d+).*')
    view_num = view_num_regex.findall(link_view)[0]
    # 文章内容,直接用html格式
    # 为什么.string返回None : http://www.crummy.com/software/BeautifulSoup/bs4/doc/#string
    #article_content = soup.find(name="div", attrs={"class":"article_content"}).string
    article_content = soup.find(name="div", attrs={"class":"article_content"}).prettify()
    #print "title###%s, post_date###%s, view_num###%s, tag###%s, article_content###%s" % (title, post_date, view_num, tag, article_content)
    info_dict = {
        "title" : title,
        "view_num" : view_num,
        "post_date" : post_date,
        "content" : article_content
    }
    return info_dict

def crawl(url, id):
    # 本地文件
    f = open('data/article_'+str(id)+'.html', 'wb+')
    content = f.read()
    if not content:
        content = getContent(url+str(id))
        f.write(content)
    if not content:
        print "http request get null----"
        return None
    msg = parseContent(content)
    f.close()
    return msg 

"""
初始化数据库
"""
def init_db():
    #数据库连接参数  
    dbconfig = { 
        'host':'localhost', 
        'port': 3306, 
        'user':'your_username', 
        'passwd':'your_password!', 
        'db':'your_dbname!'
        'charset':'utf8'
    }
    #连接数据库，创建这个类的实例
    db = MySQL(dbconfig)
    return db


"""
插入数据库
"""
def insert_db(db, r):
   title     = db.escapeString(r["title"])
   content   = db.escapeString(r["content"])
   post_date = r["post_date"]
   view_num  = r["view_num"]
   sql = "INSERT INTO %s (title,content,post_date,view_num) VALUES('%s','%s','%s',%s);" % (tablename,title,content,post_date,view_num)
   ret = db.insert(sql)


"""
主逻辑
"""    
if __name__ == '__main__':
    #获取所有文章id
    #getAllIds()

    #init_db()

    queue = Queue.Queue()
    for i in range(thread_num):
        t = downloadThread(queue)
        t.setDaemon(True)
        t.start()

    # fill in queue
    f = open("data/id_list", 'r')
    f_list = f.readlines()
    for line in f_list:
        id = line.strip()                     
        #判断是否是空行或注释行           
        if not len(id) or id.startswith('#'): 
            continue                                   
        queue.put(id)
    f.close()
    # wait for queue emtpy
    queue.join()
