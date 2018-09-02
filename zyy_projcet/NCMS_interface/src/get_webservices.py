#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2017-09-21

@author: leoinpisces
'''

import sys
import os
import re
import datetime
from suds.client import Client


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#新农合webservice的访问地址
G_url = 'http://114.255.123.85:9318/dataExchange/services/RTJSService?wsdl'

#新农合登录用户名
G_username = 'cqszyy318'

#新农合登录密码
G_password = 'rtjs'

#新农合医院代码
G_hospital_id = '450384582'

#接口调取时间
G_invoke_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#函数-python内部用的是unicode 以utf-8解码 转换为可读的汉字
def convert(str):
    return str.decode('utf-8', 'ignore')

#获取新农合webservice服务对象
def U_get_services(url):
    web_services = None
    if url != "" and url != None:
        web_client = Client(url)
        #print web_client
        web_services = web_client.service
    return web_services

if __name__ == '__main__':
    print "OK"
    pass