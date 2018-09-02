#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import utilities
import Q210
import Q230
import Q240
import Q250
import Q260
import Q260
import Q270
import Q280
import Q290
import Q299
import Q320
import Q330
import Q340
import Q360
import Q370
import Q390
import Q400
import Q410
import Q420
import time
import datetime


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

def do_job(Qxx_obj, bussiess_no):
    #添加更新日志日期的内容 20180121 李浩
    utilities.reset_log_date()
    package_processor = utilities.package_process(bussiess_no)
    package_processor.set_package(Qxx_obj)
    package_processor.sent_package()
    
#上传住院患者费用
def upload_impatient():
    #按顺序执行相关交易
    Qxx_obj = Q210.Q210()
    do_job(Qxx_obj, "Q210")
    
    Qxx_obj = Q250.Q250()
    do_job(Qxx_obj, "Q250")
    
    #Qxx_obj = Q230.Q230()
    #do_job(Qxx_obj, "Q230")
    
    Qxx_obj = Q290.Q290()
    do_job(Qxx_obj, "Q290")
    
    #Qxx_obj = Q240.Q240()
    #do_job(Qxx_obj, "Q240")
    
    #Qxx_obj = Q270.Q270()
    #do_job(Qxx_obj, "Q270")
    
#主逻辑流程    
def main_process(run_count):
    print "%s 开始本日第%d次执行".decode('utf-8').encode('cp936') % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), run_count)
    
    #只在凌晨两点到三点之间上传住院患者数据
    #time_begin = datetime.time(02,00,00)
    time_begin = 20000
    time_end = 40000
    now_time = int(time.strftime("%H%M%S"))
    
    if now_time > time_begin and now_time < time_end:
        print "开始上传住院患者数据".decode('utf-8').encode('cp936')
        upload_impatient()
    
    #Qxx_obj = Q260.Q260()
    #do_job(Qxx_obj, "Q260")
    
    #Qxx_obj = Q280.Q280()
    #do_job(Qxx_obj, "Q280")
    
    #上传门诊患者费用
    Qxx_obj = Q299.Q299()
    do_job(Qxx_obj, "Q299")
    
    #Qxx_obj = Q320.Q320()
    #do_job(Qxx_obj, "Q320")
    
    #Qxx_obj = Q330.Q330()
    #do_job(Qxx_obj, "Q330")
    
    #Qxx_obj = Q340.Q340()
    #do_job(Qxx_obj, "Q340")
    
    #Qxx_obj = Q360.Q360()
    #do_job(Qxx_obj, "Q360")
    
    #Qxx_obj = Q370.Q370()
    #do_job(Qxx_obj, "Q370")
    
    #Qxx_obj = Q390.Q390()
    #do_job(Qxx_obj, "Q390")
    
    #Qxx_obj = Q400.Q400()
    #do_job(Qxx_obj, "Q400")
    
    #Qxx_obj = Q410.Q410()
    #do_job(Qxx_obj, "Q410")
    
    #Qxx_obj = Q420.Q420()
    #do_job(Qxx_obj, "Q420")

    print "%s 本日第%d次执行完毕".decode('utf-8').encode('cp936') % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), run_count)	
    
if __name__ == '__main__':
    #程序运行计数器
    run_count = 1
    #程序的初始运行日期
    init_date = datetime.date.today()
    while True:
        cycle_date = datetime.date.today()
        #如果跨天了 更新初始运行时间 更新计数器
        if cycle_date > init_date:
            init_date = cycle_date
            run_count = 1 
        main_process(run_count)
        run_count = run_count + 1
        time.sleep(3600)

    