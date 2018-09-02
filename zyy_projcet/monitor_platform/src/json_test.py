#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import json
from uuid import UUID


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#首部需要的字段
header_210_field = ["clientmacAddress", "receiverName", "recordCount", "receiverCode", "senderCode", "intermediaryName", 
            "senderName", "hosorgNum", "busenissType", "hosorgName", "standardVersionCode", 
            "systemType", "busseID", "intermediaryCode", "sendTradeNum"]

#首部字段的默认值
header_210_default = ["", "重庆卫计委", "1", "100000001", "400057716", "", 
                      "cqszyy", "", "8", "", "version:1.0.0", 
                      "1", "Q210", "", ""] 

#附加信息字段
additioninfo_field = ["curDllAddr", "receiverTradeNum", "asyncAsk", "errorCode", "callback", "correlationId",  "errorMsg"]

#附加信息字段的默认值
additioninfo_default = ["", "", "0", "0", "", "", "" ]

#消息体列表
G_body_list = []


#以下为Q210特有部分
#消息体需要的字段
body_field = ["birthday", "inHosDoctorName", "Email", "gender", "companyName", "referralHosName", "clientStatus", 
              "guardianIdNo", "remark", "treatDate", "linkmanMobile", "medicalNum", "bunkId", "credentialNum", 
              "guardianName", "updateBy", "siType", "conditionDescription", "treatDeptCode", "homeAddress", 
              "race", "referralHosCode", "guardianIdType", "inHospitalRoute", "endemicArea", "linkmanName", 
              "inHospitalNum", "credentialType", "specialpatientID", "medicalType", "name", "reservationType", 
              "treatDeptName", "inHosDoctorCode", "additionalDiagnosisList"]

#消息体字段的默认值
body_default = ["19570929", "王某", "test@outlook.com", "2", "天马公司", "沙坪坝区人民医院", "10", 
                "", "", "20171009100700", "18612345678", "1106562", "14", "512923195709299999", 
                "", "赖宣昊", "3", "", "11", "重庆市长江路123号", 
                "01", "1260001", "", "1", "11011", "赖某某", 
                "1578124", "01", "0", "21", "郑**", "0", 
                "耳鼻咽喉科", "1002", [] ]

#诊断条目
diagnosis_item = ["diagnosisName", "diagnosisType", "diagSort", "diagnosisCode", "clinicalDiagnosis"]

#诊断条目的默认值
diagnosis_default = ["胸腔积液", "0", "0", "J94.804", "胸腔积液"]

class package():
    def __init__(self):
        self.data_header = data_header()
        self.data_addtional_info = data_addtional_info()
        self.packet_dict = {}
    
    #genflag表明生成数据包的方式 为0 则使用默认值生成 为一则使用真实数据生成数据  成功返回0 否则返回-1   
    def assumble_package(self, gen_flag):
        
        if gen_flag == 0:
            self.data_header.fill_default()
            self.data_addtional_info.fill_default()
        else:
            if len(self.data_header.header_dict) == 0 or len(G_body_list) == 0 or len(self.data_addtional_info.addtion_info) == 0:
                return -1
        
        #组装package的字典
        temp_dict = {}
        temp_dict["head"] = self.data_header.header_dict
        temp_dict["additionInfo"] = self.data_addtional_info.addtion_info
        temp_dict["body"] = G_body_list
        self.packet_dict["package"] = temp_dict
        
        return 0            

#报文首部
class data_header():
    def __init__(self):
        self.header_dict = {}
    
    def fill_default(self):
        for index in range(len(header_210_field)):
            self.header_dict[header_210_field[index]] = header_210_default[index]
        
#报文体
class data_body():
    def __init__(self):
        self.body_dict = {}
        
    def fill_default(self):
        for index in range(len(body_field)):
            self.body_dict[body_field[index]] = body_default[index]
        
        temp_dict = {}
        for inner_index in range(len(diagnosis_item)):
            temp_dict[diagnosis_item[inner_index]] = diagnosis_default[inner_index]
        self.body_dict["additionalDiagnosisList"].append(temp_dict)
            
        
#报文附加信息
class data_addtional_info():
    def __init__(self):
        self.addtion_info = {}
        
    def fill_default(self):
        for index in range(len(additioninfo_field)):
            self.addtion_info[additioninfo_field[index]] = additioninfo_default[index]
            
#生成测试报文
def gen_test_json():
    package_test = package()
    #先组装body_list
    for index in range(2):
        temp_obj = data_body()
        temp_obj.fill_default()
        G_body_list.append(temp_obj.body_dict)
    
    package_test.assumble_package(0)
    json_str = json.dumps(package_test.packet_dict, sort_keys = False, indent = 4)
    return json_str

if __name__ == '__main__':
    package_test = package()
    #先组装body_list
    for index in range(2):
        temp_obj = data_body()
        temp_obj.fill_default()
        G_body_list.append(temp_obj.body_dict)
    
    package_test.assumble_package(0) 
    
    json_str = json.dumps(package_test.packet_dict, sort_keys = False, indent = 4)
    print json_str
