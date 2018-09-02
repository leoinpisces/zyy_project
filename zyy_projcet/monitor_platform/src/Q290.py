#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import utilities

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#Q290报文body中值为字符串的key名称
G_body_keys = ["medicalNum", "billNum", "invoiceNO", "medicalType", "settleDate", "dischDate", "dischCause", "complication", "hospitalDay", 
               "sumMoney", "updateBy", "directServiceMark", "specialpatientID", "siType"]

#G_body_keys需查询的数据表
G_body_table = "V_Q290"

#标识G_body_table中一条数据的索引
G_body_index = ["medicalNum", "billNum"]

#Q290报文body中值为列表的key以及对应列表元素的名称
G_array_key = {"additionalDiagnosisList":["diagnosisCode", "diagnosisName", "clinicalDiagnosis", "diagnosisType", "diagSort"], 
               "recipeSerialNumList":["recipeSerialNum"], 
               "composite":["selfCareAmount", "selfAmount", "inInsureMoney", "medicareFundCost", "medicarePayLine", "perBearMoney", 
                            "hosBearMoney", "priorBurdenMoney", "sectionCoordinatePayMoney", "overCappingPayMoney", "fundMoney", 
                            "civilServantFundMoney", "seriousFundMoney", "accountFundMoney", "civilSubsidy", "otherFundMoney", "cashMoney"]}

#Q290报文body中值为列表的数据 所在的数据表名称 结构为{'key值':'数据表名称'}
G_array_table = {"additionalDiagnosisList":"V_Q290_DiagnosisList", "recipeSerialNumList":"V_Q290_SerialNumList", "composite":"V_Q290_SI" }

#标识G_array_table中一条数据的索引
G_array_index = {"additionalDiagnosisList":["medicalNum", "billNum"], "recipeSerialNumList":["medicalNum", "billNum"], 
                 "composite":["medicalNum", "billNum"]}

class Q290(utilities.package):
    def __init__(self):
        utilities.package.__init__(self, G_body_keys, G_body_table, G_body_index, G_array_key, G_array_table, G_array_index)
        self.bussiness_id = "Q290"
    
    
if __name__ == '__main__':
    Q290_obj = Q290()
    #生成包处理对象设置包类型
    package_processor = utilities.package_process("Q290")
    package_processor.set_package(Q290_obj)
    package_processor.sent_package()
