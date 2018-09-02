#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import utilities

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#Q299报文body中值为字符串的key名称
G_body_keys = ["medicalNum", "billNum", "medicalType", "treatDate", "endemicArea", "deptNum", "deptName", "outpatientNumber", 
               "specialpatientID", "reservationType", "referral", "siType", "doctorName", "credentialType", "credentialNum", 
               "name", "gender", "birthday", "race", "homeAddress", "companyName", "sumMoney", "updateBy", "invoiceNO", 
               "directServiceMark", "email", "linkmanName", "linkmanMobile", "guardianName", "guardianIdType", "guardianIdNo", "remark"]

#G_body_keys需查询的数据表
G_body_table = "V_Q299"

#标识G_body_table中一条数据的索引
G_body_index = ["medicalNum", "billNum"]

#Q299报文body中值为列表的key以及对应列表元素的名称
G_array_key = {"additionalDiagnosisList":["diagnosisCode", "diagnosisName", "clinicalDiagnosis", "diagnosisType", "diagSort"], 
               "recipeList":["listCat", "medicalItemCat", "recipeNum", "recipeSerialNum", "recipeDate", "productName", "englishName", 
                             "hospitalChargeCode", "hospitalChargeName", "priceitemCode", "centreChargeCode", "medicareFeeitemName", 
                             "price", "quantity", "money", "hosBearMoney", "formulation", "spec", "standardUnit", "herbFuFangSign", 
                             "totalSelfFundFlg", "extraRecipeFlg", "usage", "perQuantity", "frequency", "days", "packetNum", 
                             "medicationRoute", "deptNum", "deptName", "doctorCode", "doctorName", "selfPayRatio", "medlimitedPrice"], 
               "composite":["selfCareAmount", "selfAmount", "inInsureMoney", "medicareFundCost", "medicarePayLine", "perBearMoney", 
                            "hosBearMoney", "priorBurdenMoney", "sectionCoordinatePayMoney", "overCappingPayMoney", "fundMoney", 
                            "civilServantFundMoney", "seriousFundMoney", "accountFundMoney", "civilSubsidy", "otherFundMoney", "cashMoney"]}

#Q299报文body中值为列表的数据 所在的数据表名称 结构为{'key值':'数据表名称'}
G_array_table = {"additionalDiagnosisList":"V_Q299_DiagnosisList", "recipeList":"V_Q299_recipeList", "composite":"V_Q299_SI"}

#标识G_array_table中一条数据的索引
G_array_index = {"additionalDiagnosisList":["medicalNum", "billNum"], "recipeList":["medicalNum", "billNum"], 
                 "composite":["medicalNum", "billNum"]}

class Q299(utilities.package):
    def __init__(self):
        utilities.package.__init__(self, G_body_keys, G_body_table, G_body_index, G_array_key, G_array_table, G_array_index)
        self.bussiness_id = "Q299"
    
    
if __name__ == '__main__':
    Q299_obj = Q299()
    #生成包处理对象设置包类型
    package_processor = utilities.package_process("Q299")
    package_processor.set_package(Q299_obj)
    package_processor.sent_package()