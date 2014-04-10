#!/usr/bin/env python
#coding=utf8
from threading import Thread,Lock
from Queue import Queue
import time
import urllib2


task_num = 10000
url="http://www.baidu.com?id="
thread_num = 10
lock = Lock()

def init_queue(n):
    q = Queue(n)
    for x in range(10):
        q.put(x)
    return q

def do_stuff(i, q):
    while not q.empty():
        lock.acquire()
        id = q.get()
        response = urllib2.urlopen(url+str(id))
        print response.getcode()
        q.task_done()
        lock.release()
        # time.sleep()可以使一个线程挂起，强制线程切换发生,thread.join()会来检查当前线程是否退出
    return

def main():
    q = Queue()
    for x in range(task_num):
        q.put(x)
    start_time = time.time()
    do_stuff(1, q)
    print "time cost: %s" % (time.time() - start_time)
    return

if __name__ == '__main__':
    main()
