#!/usr/bin/python
# -*- coding: utf-8 -*-

#为了相除得到浮点数 需导入此模块
from __future__ import division
import sys
import os
import re
import datetime
import string
import threading
import random
from Queue import Queue
import time


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

G_lock = threading.Lock()

class producer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name = t_name)
        self.data = queue
    
    def run(self):
        G_lock.acquire()
        print "%s---%s acquired lock" % (time.ctime(), self.getName())
        for i in range(1000):            
            random_num = random.randint(1,99)
            print "%s---%s is producing %d and putting it into queue" % ( time.ctime(), self.getName(), random_num )
            self.data.put(random_num)
            
        G_lock.release()
        print "%s---%s release lock" % (time.ctime(), self.getName())
        
        print "%s---%s finish the job" % ( time.ctime(), self.getName() )
        
        
class consumer_even(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name = t_name)
        self.data = queue
        
    def run(self):
        while True:
                G_lock.acquire()
                #print "%s---%s acquired lock" % (time.ctime(), self.getName())
                
                if self.data.empty():
                    print "%s---%s consuming complete." % (time.ctime(), self.getName())
                    #print "%s---%s release lock" % (time.ctime(), self.getName())
                    G_lock.release()
                    break
                else:
                    val_even = self.data.get_nowait() #block = 1, timeout = 1s
                    if val_even % 2 == 0:
                        print "%s---%s consuming. %d is got from queue" % (time.ctime(), self.getName(), val_even)
                        self.data.task_done()
                    else:
                        self.data.put(val_even)
                        print "%s---%s get no even" % (time.ctime(), self.getName())
                        
                    #print "%s---%s release lock" % (time.ctime(), self.getName())
                    G_lock.release()
        return

class consumer_odd(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name = t_name)
        self.data = queue
        
    def run(self):
        while True:
                G_lock.acquire()
                #print "%s---%s acquired lock" % (time.ctime(), self.getName())
                
                if self.data.empty():
                    print "%s---%s consuming complete." % (time.ctime(), self.getName())
                    #print "%s---%s release lock" % (time.ctime(), self.getName())
                    G_lock.release()
                    break
                else:
                    val_even = self.data.get_nowait() #block = 1, timeout = 1s
                    if val_even % 2 != 0:
                        print "%s---%s consuming. %d is got from queue" % (time.ctime(), self.getName(), val_even)
                        self.data.task_done()
                    else:
                        self.data.put(val_even)
                        print "%s---%s get no odd" % (time.ctime(), self.getName())
                        
                    #print "%s---%s release lock" % (time.ctime(), self.getName())
                    G_lock.release()
        return
            
def main_thread():
    queue = Queue()
    producer_1= producer("Producer", queue)
    consumer_even_list = []
    consumer_odd_list = []
    
    for index in range(100):
        even_thread = consumer_even( ("Consumer_even_%s" % index), queue )
        consumer_even_list.append(even_thread)
        
        odd_thread = consumer_odd( ("Consumer_odd_%s" % index), queue )
        consumer_odd_list.append(odd_thread)
    
    producer_1.start()
    for index in range(len(consumer_even_list)):
        consumer_even_list[index].start()
    for index in range(len(consumer_odd_list)):
        consumer_odd_list[index].start()
    

    producer_1.join()
    #queue.join()
    
    for index in range(len(consumer_even_list)):
        consumer_even_list[index].join()
    for index in range(len(consumer_odd_list)):
        consumer_odd_list[index].join()

    print "%s---All threads is finished" % time.ctime()
    
if __name__ == '__main__':
    start_time = time.ctime()
    main_thread()
    print "program begin at %s and end at %s"  % (start_time, time.ctime())
    