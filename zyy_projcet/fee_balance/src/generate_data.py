#!/usr/bin/python
# -*- coding: utf-8 -*-

#为了相除得到浮点数 需导入此模块
from __future__ import division
import sys
import os
import re
import xlwt
import xlrd
import datetime
import analyse_xls as ax
import string
import random


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#表5费用名称列表
G_t5_fee_list = ['T5215','T5216','T5217','T5218','T5219','T5220','T5221','T5222','T5223','T5224','T5225',
                 'T5226','T5227','T5228','T5229','T5230','T5231','T5232','T5233','T5234','T5235','T5236',
                 'T5237','T5238','T5239','T5240','T5241','T5242','T5243','T5244']

#患者费用
class patient_fee:
    def __init__(self):
        self.patient_id = ""
        self.patient_name = ""
        self.discharge_dept_code = ""
        self.day_count = 0
        self.fee_dict = {}
        self.rate = 0
        
#统计各科室总共住院日
G_day_count_dict = {}

#入参范围0-100 以给定概率返回1 e.g 如果入参为30则以30%的概率返回1 入参错误时返回-1
def generate_chance(chance):
    if chance > 100 or chance < 0:
        return -1
    if chance == 100:
        return 1
    elif chance == 0:
        return 0
    else:
        chance = chance * 100
        rand_num = random.randint(1, 10000)
        if rand_num <= chance:
            return 1
        else:
            return 0
    
#获取患者相关信息
def load_patient_info():
    from __builtin__ import int
    info_list = []
    #打开表格  遍历所有行和列 填写
    workbook = xlrd.open_workbook( (ax.G_path_prefix + r"data\key_info.xlsx").decode('utf-8', 'ignore').encode('cp936') )
    active_sheet = workbook.sheet_by_name('Sheet1')
    for row_index in range(2, active_sheet.nrows):
        temp_item = patient_fee()
        #填写基本信息
        temp_item.patient_id = active_sheet.cell(row_index, 0).value
        if type(temp_item.patient_id) == float:
            temp_item.patient_id = int(temp_item.patient_id)
            
        temp_item.patient_name = active_sheet.cell(row_index, 1).value
        temp_item.discharge_dept_code = active_sheet.cell(row_index, 3).value

        #计算住院日
        temp_date = active_sheet.cell(row_index, 2).value
        if type(temp_date) == float:
            temp_date = int(temp_date)
        admission_date = datetime.datetime.strptime(str(temp_date), "%Y%m%d")
        
        temp_date = active_sheet.cell(row_index, 3).value
        if type(temp_date) == float:
            temp_date = int(temp_date)
        discharge_date = datetime.datetime.strptime(str(temp_date), "%Y%m%d")
        
        date_delta = discharge_date - admission_date
        temp_item.day_count = date_delta.days
        #累计科室住院日 按出院科室计算
        if G_day_count_dict.has_key(temp_item.discharge_dept_code):
            G_day_count_dict[temp_item.discharge_dept_code] = G_day_count_dict[temp_item.discharge_dept_code] + temp_item.day_count
        else:
            G_day_count_dict[temp_item.discharge_dept_code] = temp_item.day_count
        info_list.append(temp_item)
    return info_list

#计算个患者住院日占科室住院日占比
def date_rate_count(info_list):
    if len(G_day_count_dict) == 0:
        return 0
    for item in info_list:
        if G_day_count_dict.has_key(item.discharge_dept_code):
            item.rate = item.day_count / G_day_count_dict[item.discharge_dept_code]
        

if __name__ == '__main__':
    #patient_info = load_patient_info()
    #date_rate_count(patient_info)
    #dept_info = ax.load_info()
    test_list = []
    for i in range(100000):
        test_list.append(generate_chance(73))

    print test_list.count(1)
    print test_list.count(0)
    