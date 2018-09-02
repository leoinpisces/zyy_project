#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime
from suds.client import Client
import base64


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#http://114.255.123.85:9318/dataExchange/services/RTJSService?wsdl
#downloadMaterialInfo(xs:string userName, xs:string password, xs:string invokeDate, xs:string hospCode, xs:int itemType, xs:int pageSize, xs:int page, xs:string year, )

def get_service(url):
    web_client = Client(url)
    print web_client
    web_services = web_client.service 
    return web_services

def test_CA():
    try:
        #services = get_service("http://192.168.202.232:8084/dataExchange/services/RTJSService?wsdl")
        services = get_service("http://192.168.248.178/CAService/services/CAService?wsdl")

        result_time_stamp = services.CreateTimeStamp(services.CreateTimeStampRequest('1234567'))
        print 'Time stamp is %s' % result_time_stamp
        
        print services.VerifyTimeStamp(result_time_stamp)
        print services.GetTimeStampInfo(result_time_stamp, 1)
        print base64.b64decode(services.GenRandom())
        print services.SignData('1234567')
        
        #print (base64.b64decode(result)).decode('utf-8', 'ignore')
        
#         #print client
#         str_today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         print str_today
#         #result = services.downloadMaterialInfo('cqszyy318', 'rtjs', str_today, '450384582', 0, 10, 5, '2016')
#         #print result
# #         result = services.downloadHospitalInfo('cqszyy318', 'rtjs', str_today, '500000')
# #         print result
# #         result = services.downloadOrgInfo('cqszyy318', 'rtjs', str_today)
# #         print result
# #         result = services.downloadDictInfo('cqszyy318', 'rtjs', str_today, '450384582')
# #         print result
#         result = services.downloadZZRecords('cqszyy318', 'rtjs', str_today, '450384582', '500000', '620101', '62010120170918800023', '620101198502230150')
#         print result
#         byte_array = bytearray(result,'utf-8')
#         print len(result)
#         print len(byte_array)
    finally:
        pass

def test_myserver():
    services = get_service("http://192.168.209.136:8000/?wsdl")
    print str(services.hello_world("abc", 5))

if __name__ == '__main__':
    #test_CA()
    test_myserver()