#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import logging

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

G_path_prefix = r"F:\temp\report_jpg\\"
G_doc_size = 731, 1022

#日志相关
G_datestr_for_log = datetime.date.today().strftime("%Y-%m-%d")
logging.basicConfig(level = logging.DEBUG, 
                    format = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s', 
                    filename = (G_path_prefix + r"log\debug_log_%s.log" % G_datestr_for_log).decode('utf-8').encode('cp936'), 
                    filemode = 'a')
G_logger = logging.getLogger('repot_logger')


#拼接部分的图片名称
#G_report_section = ['title','pic_gap', 'finding', 'diagnosis', 'signature' ]
G_report_section = ['title'] 
#写入信息的的位置
G_title_position_dict = {'serial_no':[65,95], 'ward':[220,95], 'application_no':[456,95], 'examination_date':[626,95], \
                   'patient_name':[50,120], 'patient_gender':[170,120], 'patient_age':[265,120], 'examination_part':[425,120], 'patient_source':[634,120],\
                   'doctor_name':[52,145], 'department':[170,145], 'bed_no':[326,145], 'patient_id':[433,145], 'exam_equ':[589,145]}

G_report_title = { 'serial_no':'201701020001-1','ward':'肾病科病区','application_no':'56435994','examination_date':'2017-01-02',\
                  'patient_name':'郎艳','patient_gender':'女','patient_age':'22岁','examination_part':'腹部','patient_source':'住院','doctor_name':'张旗',\
                  'department':'肾病科','bed_no':'42', 'patient_id':'363116','exam_equ':'GE LOGIQ S6' }

#将文字输出到图片,输入参数为位置字典，打印的项目，字体，ImageDraw对象，打印的内容
def draw_text(position, font, drawer, text):
    try:
        drawer.text(position, unicode(text, 'utf-8'), font = font, fill = (0,0,0,255))
        G_logger.info( "The input text is %s" % text )
    except:
        return -1
    
#画报告,输入参数为要打印的区段,要打印的信息
def draw_report(section, info, infor_font):
    #位置字典
    position_dict = ''
    #模板图片
    img = ''
    
    if section == 'title':
        try:
            position_dict = G_title_position_dict
            img = Image.open((r'%spic\%s.png' % (G_path_prefix, item)).decode('utf-8').encode('cp936'))
        except IOError:
            G_logger.error("Open Section %s Picture Failed" % section)
            return -1
    try:
        drawer = ImageDraw.Draw(img)
        keys = info.keys()
        for key in keys:
            try:
                G_logger.debug("%s is painting" % key)
                ret = draw_text(position_dict[key], info_font, drawer, info[key])
            except KeyError:
                G_logger.error("Key Error") 
                continue
            if ret == -1:
                continue
    except:
        G_logger.error( "Draw %s Failed" % section )
        return -1
    return img

if __name__ == '__main__':
    try:
        result_img = Image.new('RGBA', G_doc_size)
    except IOError:
        G_logger.error( "Generate New Picture Failed" )
      
    #字体字号
    info_font = ImageFont.truetype( (r'%spic\simsun.ttc' % G_path_prefix).decode('utf-8').encode('cp936'), 15)
    #拼接图片
    high_count = 0
    try:
        for item in G_report_section:
            try:
                temp_img = draw_report(item, G_report_title, info_font)
            except:
                continue
            
            #将填好的部分贴入大图
            if temp_img != -1:
                result_img.paste(temp_img, (0, high_count))
                high_count = high_count + temp_img.size[1]
    except IOError:
        G_logger.error("Paste Section Failed")
    try:
        result_img.show()
        result_img.save((r'%spic\result.png' % G_path_prefix).decode('utf-8').encode('cp936'))
    except IOError:
        G_logger.error("Save Report Failed")
        
        
        