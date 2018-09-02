#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
from cStringIO import StringIO
from random import randint
import time
import xlwt


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')


def read_log(file_path):
    #存储时间-内存占用大小的字典
    log_dict = {}
    #存储顺序的list
    log_order = []
    #为了计算内存合计
    tmp_memory = 0.00
    #一次记录的时刻
    time_record = ""
    #日志文件描述符
    log_file = None
    try:
        log_file = open(file_path, "r")
    except IOError:
        return log_dict
    
    for line in log_file:
        if len(line) == 0:
            continue
        line = line.decode('cp936').encode('utf-8')
        index = line.find("当前时间为:")
        
        #处理时间记录行
        if index != -1:
            index = index + len("当前时间为:")
            tmp_record = line[index:]
            tmp_record = tmp_record[:-2]
            
            index = tmp_record.find("IE未运行")
            if index != -1:
                tmp_record = tmp_record[:index]
                tmp_record = tmp_record[:-1]
                log_dict[tmp_record] = 0.00
            
            time_record = tmp_record
            log_order.append(time_record)
                
        #处理ie进程数记录
        elif line.find("IE进程数目为:") != -1: 
            index = line.find("IE进程数目为:") + len("IE进程数目为:")
            tmp_record = line[index:index + 2]
            tmp_record = tmp_record.replace(" ", "")
            try:
                log_dict[time_record] = int(tmp_record)
            except:
                log_dict[time_record] = 2
        
        #处理内存合计
        elif line.find("折合为:") != -1:
            index = line.find("折合为:") + len("折合为:")
            str_end = line.find("MB")
            tmp_record = line[index:str_end]
            tmp_memory = float(tmp_record)
            log_dict[time_record] = tmp_memory / log_dict[time_record]
            
            #时间记录清零
            time_record = ""
            tmp_memory = 0.00
    
    if log_file:
        log_file.close()
        
    return (log_dict, log_order)  
        
if __name__ == '__main__':
    path = (r"D:\IE_crash_down\IE_log\wey-explorer.log").decode('utf-8').encode('cp936')
    tmp_dict, tmp_order = read_log(path)
    for item in tmp_order:
        print "%s<====>%.2f" % (item, tmp_dict[item])