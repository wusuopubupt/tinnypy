#!/usr/bin/env python
import Queue
import threading
import urllib2
import time

task_num = 10000
thread_num = 10
url = "http://www.baidu.com?id="
# Queue是线程安全的
queue = Queue.Queue()

class WorkerThread(threading.Thread):
    """
    Worker Threads
    """
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
  
    def run(self):
        while True:
            # get task from queue
            id = self.queue.get()
            res = urllib2.urlopen(url+str(id))
            print res.getcode()
            #signals to queue job is done
            self.queue.task_done()

def main():
    #spawn a pool of threads, and pass them queue instance 
    for i in range(thread_num):
        t = WorkerThread(queue)
        t.setDaemon(True)
        t.start()
    #populate queue with data   
    for x in range(task_num):
        queue.put(x)
    #wait on the queue until everything has been processed     
    queue.join()

if __name__ == '__main__':
    start = time.time()
    main()
    print "Elapsed Time: %s" % (time.time() - start)
