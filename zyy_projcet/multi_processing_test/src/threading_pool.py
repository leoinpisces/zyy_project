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

G_lock = threading.RLock()

class thread_pool():
    def __init__(self, worker_num, queue_size = 0, result_queue_size = 0, time_out = 0):
        #工作线程数目
        self.work_num = worker_num
        #请求队列 由请求对象构成 请求对象包含了处理请求的方法
        self.req_queue = Queue(queue_size)
        #结果队列  结果队列的结构为字典 key为请求 value为值 
        self.result_queue = Queue(result_queue_size)
        #工作线程列表
        self.workers = []
        #线程等待的任务时间(任务队列为空的情况)
        self.poll_timeout = time_out
        self.load_workers()
    
    #装载工作线程    
    def load_workers(self):
        for index in range(self.work_num):
            self.workers.append( worker_thread("worker_no_%s" % index, self.req_queue, self.result_queue, self.poll_timeout) )
    
    #线程启动
    def start_workers(self):
        for worker in self.workers:
            worker.start()
    
    #线程join
    def join_workers(self):
        for worker in self.workers:
            worker.join()
    
    
#工作线程类定义
class worker_thread(threading.Thread):
    def __init__(self, thread_name, req_queue, result_queue, poll_timeout):
        #构造父类对象
        threading.Thread.__init__(self, name = thread_name)
        
        self.req_queue = req_queue
        self.result_queue = result_queue
        self.poll_timeout = poll_timeout
    
    def run(self):
        #循环运行
        while True:
            
            pass



class requst():
    def __init__(self, handler, error_handler):
        pass
    
if __name__ == 'main':
    pass