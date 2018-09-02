#!/usr/bin/python
# -*- coding: utf-8 -*-

#为了相除得到浮点数 需导入此模块
from __future__ import division
import sys
import os
import re
import string
import threading
import random
import time
import base64
from Queue import Queue
from suds.client import Client

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#任务队列锁
G_lock = threading.Lock()

#工作线程数量
G_worker_num = 600

#任务数量
G_task_num = 1000

#webservice地址
G_url = "http://192.168.248.178/CAService/services/CAService?wsdl"

#生产者具体工作函数
class producer_handler():
    def __init__(self, round_time):
        self.round_time = round_time
        
    def run(self, queue):
        for index in range(self.round_time):
            queue.put(index)
            print "put %s into queue" % index

#生产者线程定义        
class producer(threading.Thread):
    def __init__(self, t_name, queue, handler):
        threading.Thread.__init__(self, name = t_name)
        self.queue = queue
        self.handler = handler
    
    def run(self):
        G_lock.acquire()
        #print "%s---%s acquired lock" % (time.ctime(), self.getName())
        self.handler.run(self.queue)
        G_lock.release()
        #print "%s---%s release lock" % (time.ctime(), self.getName())
        print "%s---%s finish the job" % ( time.ctime(), self.getName() )
        
class consumer_handler():
    def __init__(self, url):
        self.url = url
        
    def run(self, data):
        web_client = Client(self.url)
        services = web_client.service
        result_time_stamp = services.CreateTimeStamp(services.CreateTimeStampRequest(data))
        print result_time_stamp[:15]
        
class consumer(threading.Thread):
    def __init__(self, t_name, queue, handler):
        threading.Thread.__init__(self, name = t_name)
        self.queue = queue
        self.handler = handler
        
    def run(self):
        from __builtin__ import str
        while True:
            G_lock.acquire()
            #print "%s---%s acquired lock" % (time.ctime(), self.getName())
            
            if self.queue.empty():
                print "%s---%s consuming complete." % (time.ctime(), self.getName())
                #print "%s---%s release lock" % (time.ctime(), self.getName())
                G_lock.release()
                break
            else:
                token = self.queue.get_nowait()
                self.handler.run(str(random.randint(1,10) + token))
                  
                #print "%s---%s release lock" % (time.ctime(), self.getName())
                G_lock.release()
        return
            
def main_thread():
    #生成任务队列
    queue = Queue()
    #构造生产者处理函数 指定任务数量
    handler = producer_handler(G_task_num)
    producer_1 = producer("Producer", queue, handler)
    
    consumer_list = []
    for index in range(G_worker_num):
        temp_handler = consumer_handler(G_url)
        temp_consumer = consumer( ("Consumer_%s" % index), queue, temp_handler )
        consumer_list.append(temp_consumer)
    
    #生产者线程启动
    producer_1.start()
    
    for index in range(G_worker_num):
        consumer_list[index].start()    

    producer_1.join()
    #queue.join()
    
    for index in range(G_worker_num):
        consumer_list[index].join()
    print "%s---All threads is finished" % time.ctime()
    
if __name__ == '__main__':
    start_time = time.ctime()
    main_thread()
    print "program begin at %s and end at %s"  % (start_time, time.ctime())
    

# def get_service(url):
#     web_client = Client(url)
#     #print web_client
#     web_services = web_client.service 
#     return web_services
# 
#     
# 
# if __name__ == '__main__':
#     try:
#         #services = get_service("http://192.168.202.232:8084/dataExchange/services/RTJSService?wsdl")
#         services = get_service("http://192.168.248.178/CAService/services/CAService?wsdl")
# 
#         result_time_stamp = services.CreateTimeStamp(services.CreateTimeStampRequest('1234567'))
#         print 'Time stamp is %s' % result_time_stamp
#         
#         print services.VerifyTimeStamp(result_time_stamp)
#         print services.GetTimeStampInfo(result_time_stamp, 1)
#         print base64.b64decode(services.GenRandom())
#         print services.SignData('1234567')
