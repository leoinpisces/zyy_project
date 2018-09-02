#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import xlwt
import datetime



os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

class name_id:
    name = ""
    id_no = ""
    
g_source_dict = {}
g_dest_dict = {}

g_repeat_name_list = []
g_name_order_list =[]


#函数-转换为中文操作系统可读的编码
def convert_c(convert_str):
    return convert_str.decode('utf-8').encode('cp936')

def read_dict(target_dict, file_path):
    dict_file = open(file_path, "r+")
    
    for line in dict_file:
        line = line.strip()
        if line == "":
            continue
        temp_list = line.split("!@!")
        if len(temp_list) != 2:
            continue
        
        temp_list[0] = temp_list[0].strip()
        temp_list[1] = temp_list[1].strip()
        
        if target_dict.has_key(temp_list[0]) and file_path.count("dest") >0:
            g_repeat_name_list.append(temp_list[0])
        else:
            target_dict[temp_list[0]] = temp_list[1]
    
    dict_file.close()
            
def fill_order_list(file_path):
    order_file = open(file_path, "r+")
    
    for line in order_file:
        line = line.strip()
        if line == "":
            continue
        temp_list = line.split("!@!")
        if len(temp_list) != 2:
            continue
        
        temp_list[0] = temp_list[0].strip()
        temp_list[1] = temp_list[1].strip()
        
        g_name_order_list.append(temp_list[0])
    
    order_file.close()
    

def fill_dest_dist():
    if len(g_source_dict) == 0 or len(g_dest_dict) == 0:
        return
    names = g_name_order_list
    for item in names:
        if g_source_dict.has_key(item):
            if g_dest_dict[item] == "0":
                g_dest_dict[item] = g_source_dict[item]
                
def fill_dest_excle():
    if len(g_source_dict) == 0 or len(g_dest_dict) == 0:
        return
    
    result_xls = xlwt.Workbook(encoding='cp936')
    sheet = result_xls.add_sheet('sheet 1', cell_overwrite_ok = True)
    
    line_index = 0
    for name in g_name_order_list:
        sheet.write(line_index, 0, convert_c(name))
        sheet.write(line_index, 1, g_dest_dict[name])
        line_index = line_index + 1
        
    result_xls.save( r'F:\temp\result.xls'.decode('utf-8').encode('cp936') )
                
if __name__ == '__main__':
    soure_path = r'F:\temp\source.txt'.decode('utf-8').encode('cp936')
    dest_path = r'F:\temp\dest.txt'.decode('utf-8').encode('cp936')
    
    read_dict(g_source_dict, soure_path)
    read_dict(g_dest_dict, dest_path)
    
    fill_order_list(dest_path)
    fill_dest_dist()
    fill_dest_excle()
    result_file = open(r'F:\temp\result.txt'.decode('utf-8').encode('cp936'), 'w+')
    for name in g_name_order_list:
        result_file.write(convert_c(name) + "," + convert_c(g_dest_dict[name]) + '\r')
    result_file.close()
    
    repeat_file = open(r'F:\temp\repeat_name.txt'.decode('utf-8').encode('cp936'),'w+')
    for name in g_repeat_name_list:
        repeat_file.write(convert_c(name) + '\r')
    repeat_file.close()
    
    print "OK"
    
    
    
                
                