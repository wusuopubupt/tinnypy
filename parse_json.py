#!/usr/bin/env python
#encoding=utf8
#brief: 请求url，解析json
import os
import sys
import urllib2
import json

req_url="http://zhidao.baidu.com/s/toutu/promotion.js"


"""
请求html页面数据
"""
def getContent(url):
    # 伪造header
    send_headers = {
        'Referer' : 'http://api.weipann.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    }
    req = urllib2.Request(url,headers=send_headers)
    ret = urllib2.urlopen(req)
    html = ret.read()                             
    return html 

def main():
    html = getContent(req_url)
    data = json.loads(html)
    # 判断返回dict还是list, 根据不同返回格式做不同的遍历操作
    print type(data)
    # if list
    """
    print (data)
    for k,v in enumerate(data):
        print k,v
    """
    # if dict
    print (data)
    for k,v in data.iteritems():
        print k,v

if __name__ == '__main__':
    main()

