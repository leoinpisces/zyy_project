#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import utilities

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

# #Q390报文body中值为字符串的key名称
G_body_keys = ["medicalNum", "billNum", "labNum", "recordNum", "serviceClassification", "categoryName", "findings", 
               "inspectExamResult", "patName", "sex", "patAge", "ageUnit", "diagnosis", "deptNum", "deptName", "applyDoctorCode", 
               "applyDoctorName", "bunkId", "applyDate", "reportDate", "confirmDate", "reportDoctorCode", "reportDoctorName", 
               "confirmDoctorCode", "confirmDoctorName", "sampleType", "instrna", "instrKind", "instrKindName", "insertFlag", 
               "remark", "effectiveMark"]

#G_body_keys需查询的数据表
G_body_table = "V_Q390"

#标识G_body_table中一条数据的索引
G_body_index = "medicalNum"

#Q390报文body中值为列表的key以及对应列表元素的名称
G_array_key = {"inspectionExaminationList":["itemNum", "itemName", "numVal", "txtVal", "additionVal", "pnFlag", "reference", 
                                            "insertFlag", "method1", "method2", "plasmaConcentration1", "plasmaConcentration2", 
                                            "urineConcentration1", "urineConcentration2", "drugAllergyCode", "sensitivity", 
                                            "bacteriostatDiameter"]}

#Q390报文body中值为列表的数据 所在的数据表名称 结构为{'key值':'数据表名称'}
G_array_table = {"inspectionExaminationList":""}

#标识G_array_table中一条数据的索引
G_array_index = {"inspectionExaminationList":""}

class Q390(utilities.package):
    def __init__(self):
        utilities.package.__init__(self, G_body_keys, G_body_table, G_body_index, G_array_key, G_array_table, G_array_index)
        self.bussiness_id = "Q390"
    
    
if __name__ == '__main__':
    Q390_obj = Q390()
    #生成包处理对象设置包类型
    package_processor = utilities.package_process("Q390")
    package_processor.set_package(Q390_obj)
    package_processor.sent_package()