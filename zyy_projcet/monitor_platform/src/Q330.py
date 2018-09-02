#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import utilities

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#Q330报文body中值为字符串的key名称
G_body_keys = ["diseaseCode", "diseaseName", "diseaseType", "sidiseaseCode", "sidiseaseName", "beginDate", "endDate", "remark"]

#G_body_keys需查询的数据表
G_body_table = "V_Q330"

#标识G_body_table中一条数据的索引
G_body_index = ["diseaseCode"]

#Q330报文body中值为列表的key以及对应列表元素的名称
G_array_key = {}

#Q330报文body中值为列表的数据 所在的数据表名称 结构为{'key值':'数据表名称'}
G_array_table = {}

#标识G_array_table中一条数据的索引
G_array_index = {}

class Q330(utilities.package):
    def __init__(self):
        utilities.package.__init__(self, G_body_keys, G_body_table, G_body_index, G_array_key, G_array_table, G_array_index)
        self.bussiness_id = "Q330"
    
    
if __name__ == '__main__':
    Q330_obj = Q330()
    #生成包处理对象设置包类型
    package_processor = utilities.package_process("Q330")
    package_processor.set_package(Q330_obj)
    package_processor.sent_package()