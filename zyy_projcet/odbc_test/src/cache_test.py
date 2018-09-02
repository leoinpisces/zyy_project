#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import db_connector



os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

def hello_world():
    #conn = db_connector.db_connector(dsn = "CacheTest", usrname = "_system", pwd = "SYS", db_type = "cache")
    #conn = db_connector.db_connector(dsn = "DmkHis", usrname = "dhact", pwd = "dhact@SYS", db_type = "cache")
    conn = db_connector.db_connector(dsn = "NqsHis", usrname = "dhact", pwd = "dhact@SYS", db_type = "cache")
    #sql = "SELECT * FROM dhc_workload WHERE workload_flagdate BETWEEN \"2018-02-08\" AND \"2018-02-09\""
    #sql = "SELECT MRZYWT_bah, MRZYWT_csd, MRZYWT_gg, MRZYWT_sfzh, MRZYWT_hkdz FROM dhcmrzywtfinfo"
    #sql = "SELECT InstanceData FROM EMRinstance.InstanceData where EpisodeID = 280831 AND Title = ''"
    #sql = "SELECT InstanceData FROM EMRinstance.InstanceData where EpisodeID = 437046 AND ID = '513665||4'"
    sql = "SELECT * FROM EMRinstance.InstanceData WHERE EpisodeID = 1346 AND Title = '中医病案首页'"
    
    sql = sql.decode('utf-8')
    conn.excute_sql(sql)
    res_list = conn.cache_get_content_from_lob()
    #print len(res_list)
    print res_list[0]
    #sql = "select count(1) from dhc_workload"
#     rows = conn.get_rows(sql)
#     
#     for row in rows:
#         print row[4]
#         print (row[4]).decode('utf-8', 'ignore')
#         print len(row[4])
#         print len( (row[4]).decode('utf-8', 'ignore') )
    
if __name__ == '__main__':
    hello_world()