#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cx_Oracle
import os
import re
import jieba
import xlwt
import datetime
import logging

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')


#类-产妇信息类
class puerpera_info:
    name = "" #姓名
    patient_id = "" #住院号
    id_type = "" #证件类型
    id_value = "" #证件号码
    date_of_birth = "" #出生日期
    nation = "" #国籍
    ethnicity = "" #民族
    registed_address_p = "" #户籍地址-省
    registed_address_ci = "" #户籍地址-市
    registed_address_co = "" #户籍地址-区县
    registed_address_code = "" #户籍地省-行政区划代码
    domicile_p = "" #居住地-省
    domicile_ci = "" #居住地-市
    domicile_co = "" #居住地-区县
    domicile_code = "" #居住地省-行政区划代码
    birth_place = "" #产妇出生地
    gravidity = 0 #孕次
    parity = 0 #产次
    gestational_weeks = 0 #孕周
    is_high_risk = "9" #是否高危 1是 2否 9不清楚
    delivery_mode = "" #分娩方式 1阴道产 2剖宫产
    delivery_date = "" #分娩日期
    fetus1_gender = "9" #第一胎性别 1男 2女 9不明
    fetus1_outcome = "" #第一胎分娩结局 1活产 2死胎死产
    fetus1_agpar = 0 #第一胎apgar评分
    fetus2_gender = "9" #第二胎性别
    fetus2_outcome = "" #第二胎分娩结局
    fetus2_agpar = 0 #第二胎apgar评分
    is_twin = False #标志位 判断是否双胞胎 True为双胞胎
    admission_date = "" #入院日期
    diagnosis = "" #诊断
    

G_info_list = []


#类-全局变量类 地址字典 用于分词后的地址编码识别 民族字典 用于识别产妇民族 国家名称字典 用于识别产妇国籍
class G_dictionary:
    address_dict_chongqing = {}
    address_dict_allprovince = {}
    address_dict_other = {}
    address_dict_sichuan = {}
    address_dict_guizhou = {}
    address_dict_country = {}
    nation_dict = {}
    country_name_dict = {}
    

#类-判断行政区划编码级别的正则表达式
class G_level_searcher:
    searcher_province = re.compile(r'[1-9]\d0{4}')
    searcher_city = re.compile(r'\d{2}[1-9]\d00|\d{2}\d[1-9]00')
    searcher_county = re.compile(r'\d{4}[1-9]\d|\d{4}\d[1-9]')
    

#抓取apgar评分的正则表达式
G_apgar_searcher = re.compile(r'一评二评三评均\d{1,2}分|满分|一评\d{1,2}分|[1-3]分钟评分\d{1,2}分|[1-3]分钟评\d{1,2}分|[Aa]pgar评分均\d{1,2}分')
#抓取分娩日期的正则表达式
#G_dob_searcher = re.compile(r'于\d{4}年\d{1,2}月\d{1,2}日|于\d{1,2}月\d{1,2}日|[于予]\d{4}-\d{1,2}-\d{1,2}[在行因顺经]|[于予]\d{4}-\d{1,2}-\d{1,2}日[在行因顺经]|\d{4}-\d{1,2}-\d{1,2}因|于\d{4}-\d{1,2}-\d{1,2}\d{2}\:\d{2}|患者\d{1,2}月\d{1,2}日')
G_dob_searcher = re.compile(r'于\d{4}年\d{1,2}月\d{1,2}日|于\d{1,2}月\d{1,2}日|[于予]\d{4}-\d{1,2}-\d{1,2}[在行因顺经]|[于予]\d{4}-\d{1,2}-\d{1,2}日[在行因顺经]|\d{4}-\d{1,2}-\d{1,2}因|于\d{4}-\d{1,2}-\d{1,2}\d{2}\:\d{2}')
#抓取孕次的正则表达式
G_gravidity_searcher = re.compile(r'G\d{1,2}P')
#抓取产次的正则表达式
G_parity_searcher = re.compile(r'P\d{1,2}[LR]{0,1}')
#判断新生儿是否死亡的正则表达式
G_fetus_dead_searcher = re.compile(r'新生儿死亡|死婴|死女婴|死男婴|男死婴|女死婴')
#抓取孕周的正则表达式
G_gestational_weeks_searcher = re.compile(r'\d{2}\+{0,1}[1-6]{0,1}周')
#抓取新生儿性别为“女”的正则表达式
G_female_searcher = re.compile(r'女婴|活女婴|女活婴|女死婴|死女婴')
#抓取新生儿性别为“男”的正则表达式
G_male_searcher = re.compile(r'男婴|活男婴|男活婴|死男婴|男死婴')

#获取今日的日期以命名错误日志
G_datestr_for_log = datetime.date.today().strftime("%Y%m%d")

#是否使用出院证作为数据抓取对象
G_use_discharge_certification = False

#相关文件的路径前缀
G_path_prefix = r"C:\code\\"

#函数-连接oracle数据库
def get_connection():
    user_name = 'jhemr'
    user_pwd = 'jhemr'
    host = '192.168.248.33'
    port = 1521
    service_name = 'JHEMR'
    dsn = cx_Oracle.makedsn(host, port, service_name)
    conn = cx_Oracle.connect(user_name, user_pwd, dsn)
    return conn

    
#函数-关闭数据库连接
def close_connection(conn):
    conn.cursor().close()
    conn.close()

    
#函数-python内部用的是unicode 以utf-8解码 转换为可读的汉字
def convert(str):
    return str.decode('utf-8', 'ignore')

#函数-转换为中文操作系统可读的编码
def convert_c(str):
    return str.decode('utf-8').encode('cp936')


#函数-写log的函数 目前暂时向控制台输出
def write_log(content, level):
    if level == "debug":
        print content
    if level == "error":
        file_name = (G_path_prefix + r"puerpera_data_report\error_log\error_log_%s.txt" % G_datestr_for_log).decode('utf-8').encode('cp936')
        file = open(file_name, "a+")
        file.write(content)
        file.write("\r\n")
        file.close()

        
#函数-获取患者的基本信息 包括住院号 姓名 身份证号 出生日期 国籍 民族 户口地址 现住址（如果户口地址为空则用此字段） 
#诊断名称 入院日期（如果为抓取到分娩日期则用此字段）构造对象 填入列表 G_info_list
def get_basic_info(cursor, begin_str, end_str):
    sql = "select b.patient_id, c.name, c.id_no, to_char(c.date_of_birth, 'YYYYMMDD'), c.citizenship, c.nation, b.nomen, \
    b.mailing_address, a.diagnosis_desc, to_char(b.admission_date_time, 'YYYYMMDD'), c.birth_place from pat_visit b, pat_master_index c, diagnosis a \
    where b.dept_discharge_from = '5937' \
    and b.discharge_date_time > to_date('%s', 'yyyy/mm/dd') \
    and b.discharge_date_time < to_date('%s', 'yyyy/mm/dd') \
    and b.patient_id = c.patient_id \
    and a.patient_id = b.patient_id \
    and a.diagnosis_type = '3' \
    and (a.diagnosis_desc like '妊娠%%顺产' or a.diagnosis_desc like '妊娠%%剖宫产' or a.diagnosis_desc like '孕%%顺产' or a.diagnosis_desc like '孕%%剖宫产') \
    and (c.name not like '%%之婴' or c.name not like '%%大双' or c.name not like '%%小双')" %(begin_str, end_str)
    #and a.patient_id = '405077' 
    
    cursor.execute(sql) 
    result = cursor.fetchall()
    
    #print cursor.description[0][0] #获取列名
    
    for item in result:
        if len(item) < 11:
            continue
        temp_obj = puerpera_info()
        temp_obj.name = str(item[1])
        temp_obj.patient_id = str(item[0])
        temp_obj.id_value = (str(item[2])).strip()
        #如果证件号码长度为15或18位，说明证件类型是身份证，否则证件类型为其他
        if len(temp_obj.id_value) == 18 or len(temp_obj.id_value) == 15:
            temp_obj.id_type = "1"
        else:
            temp_obj.id_type = "9"
        temp_obj.date_of_birth = str(item[3])
        
        #如果出生日期为空则从身份证号中取
        if len(temp_obj.date_of_birth) < 8:
            if len(temp_obj.id_value) == 18:
                temp_obj.date_of_birth = temp_obj.id_value[6:14]
            elif len(temp_obj.id_value) == 15:
                temp_obj.date_of_birth = "19" + temp_obj.id_value[6:12]
        
        temp_obj.nation = (str(item[4])).strip()
        temp_obj.ethnicity = (str(item[5])).strip()
        temp_obj.registed_address_p = (str(item[6])).strip()
        temp_obj.domicile_p = (str(item[7])).strip()
        temp_obj.diagnosis = (str(item[8])).strip()
        temp_obj.admission_date = (str(item[9])).strip()
        temp_obj.birth_place = (str(item[10])).strip()
        
        #根据诊断内容判断分娩方式 1为阴道产 2为剖宫产
        if temp_obj.diagnosis.count("顺产") > 0:
            temp_obj.delivery_mode = "1"
        else:
            temp_obj.delivery_mode = "2"
        
        #判断是否双胞胎
        temp_obj = set_twin_flag(temp_obj, cursor)
        G_info_list.append(temp_obj)

#判断是否双胞胎
def set_twin_flag(item, cursor):
    sql = "select diagnosis_desc from diagnosis where patient_id = '%s' and diagnosis_desc like '双胎%%'" % item.patient_id
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) > 0:
        item.is_twin = True
    else:
        item.is_twin = False
        
    return item
        

#函数-处理地址 包括户口地址和现住址
def address_process(item):
    if item.registed_address_p == "None" or item.registed_address_p == "同上" or item.registed_address_p == "不详":
        item.registed_address_p = item.domicile_p
    if item.registed_address_p == "None" or item.registed_address_p == "同上" or item.registed_address_p == "不详":
        item.registed_address_p = item.birth_place
    if item.registed_address_p == "None":    
        return
        
    #处理户籍地址
    seg_list = list(jieba.cut(item.registed_address_p, cut_all = False))
    result_list = get_code_from_dict(seg_list)
    for inner_item in result_list:
        if get_code_level(inner_item) == 3:
            if G_dictionary.address_dict_country.has_key(inner_item):
                item.registed_address_p = G_dictionary.address_dict_country[inner_item]
            item.registed_address_code = inner_item
        elif get_code_level(inner_item) == 2:
            if G_dictionary.address_dict_country.has_key(inner_item):
                item.registed_address_ci = G_dictionary.address_dict_country[inner_item]
        elif G_dictionary.address_dict_country.has_key(inner_item):
            item.registed_address_co = G_dictionary.address_dict_country[inner_item]
    
    #处理现住址
    seg_list = list(jieba.cut(item.domicile_p, cut_all = False))
    result_list = get_code_from_dict(seg_list)
    for inner_item in result_list:
        if get_code_level(inner_item) == 3:
            if G_dictionary.address_dict_country.has_key(inner_item):
                item.domicile_p = G_dictionary.address_dict_country[inner_item]
            item.domicile_code = inner_item
        elif get_code_level(inner_item) == 2:
            if G_dictionary.address_dict_country.has_key(inner_item):
                item.domicile_ci = G_dictionary.address_dict_country[inner_item]
        elif G_dictionary.address_dict_country.has_key(inner_item):
            item.domicile_co = G_dictionary.address_dict_country[inner_item]
            

#函数-遍历    G_info_list 总装数据
def build_info(cursor):
    if len(G_info_list) == 0:
        return
    
    #初始化地址字典
    load_address_dict("重庆")
    load_address_dict("四川")
    load_address_dict("贵州")
    load_address_dict("省份字典")
    load_address_dict("全国")
    
    load_dict("country_dict")
    load_dict("nation_dict")
    
    for item in G_info_list:
        #处理户籍地址和居住地
        address_process(item)
        
        #处理产妇民族
        item.ethnicity = get_ethnicity(item.ethnicity)
        #处理产妇国籍
        item.nation = get_nation(item.nation)
        
        #处理孕周
        temp_week_str = get_gestational_weeks(item.diagnosis)
        if temp_week_str != "" and temp_week_str.isdigit():
            item.gestational_weeks = int(temp_week_str)
            
        #处理孕次产次
        gp_pair = get_GP(item.diagnosis)
        item.gravidity = int(gp_pair[0])
        item.parity = int(gp_pair[1])
        #处理医生写错了产次的
        if item.parity == 0:
            item.parity = 1
        
        #提取产妇出院证或相关提取文档
        result_list = get_discharge_certificate(item, cursor)
        if len(result_list) < 1:
            continue
        dc_file = result_list[0]
        print convert(dc_file)
        
        #处理分娩日期
        dob_str = get_dob(G_dob_searcher.findall(dc_file))
        if len(dob_str) == 4:
            dob_str = item.admission_date[0:4] + dob_str
        item.delivery_date = dob_str
        
        #如果未抓取到有效的分娩时间  则从数据库中寻找相关文档的caption_date_time
        if item.delivery_date == "":
            item.delivery_date = get_caption_time(item.patient_id, item.delivery_mode, cursor)
        
        #判断是否高危产妇
        item.is_high_risk = is_high_risk(dc_file)
        
        #处理apgar评分
        #print convert(dc_file)
        apgar_list = get_apgar(G_apgar_searcher.findall(dc_file))
        write_log(convert( "apgar_list列表长度: " + str(len(apgar_list)) ) , "debug")
        #单胎
        if not item.is_twin:
            if len(apgar_list) < 1:
                write_log("Wrong apgar_list length", "debug")
                if dc_file.count("产程顺利") > 0:
                    item.fetus1_agpar = 10
            elif apgar_list[0].isdigit():
                item.fetus1_agpar = int(apgar_list[0])
        #双胞胎
        else:
            if len(apgar_list) < 1:
                write_log("Wrong apgar_list length", "debug")
                if dc_file.count("产程顺利") > 0:
                    item.fetus1_agpar = 10
                    item.fetus2_agpar = 10
            elif len(apgar_list) < 2:
                write_log("Wrong apgar_list length", "debug")
                if apgar_list[0].isdigit():
                    item.fetus1_agpar = int(apgar_list[0])
                    item.fetus2_agpar = int(apgar_list[0])
            else:
                if apgar_list[0].isdigit():
                    item.fetus1_agpar = int(apgar_list[0])
                if apgar_list[1].isdigit():
                    item.fetus2_agpar = int(apgar_list[1])
                    
        #如果没有抓取到apgar评分 或分娩日期 将产妇出院证写入错误日志以供分析
        if item.fetus1_agpar == 0:
            write_log("missing agpar           " + dc_file, "error")
        if len(item.delivery_date) < 8:
            write_log("missing delivery date   " + dc_file, "error")
        
        #判断分娩结局
        count_num = len(G_fetus_dead_searcher.findall(dc_file))
        #count_num大于0 说明存在死胎的情况  
        if count_num > 0:
            #处理单胎的情况  apgar评分的初始值是0
            if not item.is_twin:
                item.fetus1_outcome = "2"
            #处理双胞胎的情况 如果apgar一评小于4分 程序认为该新生儿死亡
            if item.is_twin:
                if item.fetus1_agpar < 4:
                    item.fetus1_outcome = "2"
                if item.fetus2_agpar < 4:
                    item.fetus2_outcome = "2"
        else:
            item.fetus1_outcome = "1"
            if item.is_twin:    
                item.fetus2_outcome = "1"
        
        #处理胎儿性别
        result_list = []
        result_list = get_fetus_gender_from_dc(dc_file)
        
        if len(result_list) == 0:
            #如果出院证没有写明胎儿性别 则需要从数据库中查找胎儿信息 可信度相对较低
            result_list = get_fetus_gender_from_database(item.name, item.admission_date, item.is_twin, cursor)
            
        if len(result_list) == 0:
            item.fetus1_gender = "9"
            if item.is_twin:
                item.fetus2_gender = "9"
        else:
            item.fetus1_gender = result_list[0]
            if item.is_twin and len(result_list) > 1:
                item.fetus2_gender = result_list[1]
            elif item.is_twin and len(result_list) == 1:
                item.fetus2_gender = result_list[0]
            else:
                item.fetus2_gender = "9"


#函数-获取相关文档的caption_date_time 未抓取到分娩时间时使用
def get_caption_time(patient_id, delivery_mode, cursor):
    if len(patient_id) < 6:
        return ""
    #顺产提分娩记录
    if delivery_mode == "1":
        sql = "select to_char(caption_date_time,'YYYYMMDD') from jhmr_file_index where patient_id = '%s' and topic like '%%分娩记录%%'" % patient_id
    #剖宫产提术后首程记录
    elif delivery_mode == "2":
        sql = "select to_char(caption_date_time,'YYYYMMDD') from jhmr_file_index where patient_id = '%s' and topic like '%%术后首次病程记录%%'" % patient_id
    else:
        return ""
    cursor.execute(sql)
    result = cursor.fetchall()
    
    if len(result) < 1:
        return ""
    
    for item in result:
        if len(item[0]) == 8:
            return item[0]
        

#函数-判断是否高危产妇1是2否9不清楚
def is_high_risk(dc_file):
    if len(dc_file) < 4:
        return "9"
    count = dc_file.count("高危妊娠:是")
    if count > 0:
        return "1"
    else:
        return "2"


#函数-从出院证中获取胎儿性别
def get_fetus_gender_from_dc(dc_file):
    female_count = len(G_female_searcher.findall(dc_file))        
    male_count = len(G_male_searcher.findall(dc_file))
    result_list = []
    #1代表男婴 用2代表女婴
    for index in range(0, female_count):
        result_list.append("2")
    for index in range(0, male_count):
        result_list.append("1")
    return result_list

            
#函数-从数据库中获取胎儿性别 无法处理母亲同名同姓的问题
def get_fetus_gender_from_database(name, admission_date, is_twin, cursor):
    result_list = []
    #处理单胎
    if not is_twin:
        sql = "select a.sex, to_char(b.admission_date_time, 'YYYYMM') from pat_master_index a, pat_visit b \
        where (a.name = '%s之婴' or a.name = '%s之子' or a.name = '%s之女') \
        and a.patient_id = b.patient_id and a.inp_no is not null" %(name, name, name)
        cursor.execute(sql)
        result = cursor.fetchall()
        
        for item in result:
            if len(item) < 2:
                continue
            #确保单胎只有一个性别写回
            if len(result_list) > 0:
                break
            sex = str(item[0]).strip()
            ad_date = str(item[1]).strip()
            #要求新生儿的入院日期(精确到月)与母亲一致
            if str(ad_date) == admission_date[0:6]:
                if sex == "男":
                    result_list.append("1")
                elif sex == "女":
                    result_list.append("2")
    #处理双胞胎
    else:
        sql = "select a.sex, to_char(b.admission_date_time, 'YYYYMM') from pat_master_index a, pat_visit b \
        where (a.name = '%s之大双' or a.name = '%s之小双') \
        and a.patient_id = b.patient_id and a.inp_no is not null" %(name, name)
        cursor.execute(sql)
        result = cursor.fetchall()
        for item in result:
            if len(item) < 2:
                continue
            #确保双胞胎只有两个性别写回
            if len(result_list) > 1:
                break
            sex = str(item[0]).strip()
            ad_date = str(item[1]).strip()
            if str(ad_date) == admission_date[0:6]:
                if sex == "男":
                    result_list.append("1")
                elif sex == "女":
                    result_list.append("2")
    return result_list


#函数-获取分娩日期 合法的日期格式为YYYYMMDD或MMDD
def get_dob(dob_list):
    if len(dob_list) < 1:
        return ""
    dob_str = ""
    for item in dob_list:
        dob_str = DOB_process(item)
        if len(dob_str) == 8 or len(dob_str) == 4:
            break
    if dob_str == "":
        return ""
    #处理因为编码问题导致的正则抓取一半汉字情况
    elif len(dob_str) > 8:
        temp_str = dob_str
        for index in range(len(temp_str)):
            if temp_str[index].isdigit():
                continue
            else:
                dob_str = dob_str.replace(temp_str[index], "")
        return dob_str
    else:
        return dob_str

#函数-获取新生儿apgar评分 可处理单胎和双胞胎的情况
def get_apgar(apgar_list):
    result_list = []
    if len(apgar_list) < 1:
        write_log(convert("apgar_list正则抓取错误"), "debug")
        return result_list
    for item in apgar_list:
        temp_str = apgar_process(item)
        if temp_str != "":
            result_list.append(temp_str)
    return result_list

#函数-获取产妇民族编码
def get_ethnicity(ethnicity):
    #如果未填写产妇民族 默认返回汉族
    if ethnicity == "":
        return "01"
    ethnicity = ethnicity.strip()
    if G_dictionary.nation_dict.has_key(ethnicity):
        return G_dictionary.nation_dict[ethnicity]
    #字典中找不到的也默认为汉族
    else:
        return "01"

#函数-获取产妇国籍编码
def get_nation(country_name):
    #如果未填写国籍名称 默认返回中国
    if country_name == "":
        return "CHN"
    country_name = country_name.strip()
    if G_dictionary.country_name_dict.has_key(country_name):
        return G_dictionary.country_name_dict[country_name]
    #字典中找不到的也默认为中国
    else:
        return "CHN"
        
#函数-获取孕周
def get_gestational_weeks(diagnosis):
    if diagnosis == "":
        return ""
    result_list = G_gestational_weeks_searcher.findall(diagnosis)
    if len(result_list) < 1:
        return ""
    week_str = result_list[0]
    if week_str.count("+") > 0:
        temp_list = week_str.split("+")
        week_str = temp_list[0]
    else:
        week_str = week_str.replace("周", "")
    return week_str

#函数-获取孕次产次
def get_GP(diagnosis):
    if diagnosis == "":
        return(0,0)
        
    diagnosis = diagnosis.strip()
    diagnosis = diagnosis.replace(" ", "")
    
    temp_list = G_gravidity_searcher.findall(diagnosis)
    if len(temp_list) < 1:
        return(0,0)
    temp_g = temp_list[0].replace("G", "").replace("P", "")
    if len(temp_g) < 1:
        return (0,0)
    
    temp_list = G_parity_searcher.findall(diagnosis)
    if len(temp_list) < 1:
        return(0,0)
    temp_p = temp_list[0].replace("P", "").replace("R", "").replace("L", "")
    if len(temp_g) < 1:
        return (0,0)
    
    return (temp_g, temp_p)


#函数-从lob字段中获取内容
def get_content_from_lob(cursor):
    result_list = []
    for row in cursor:
        content_list = []
        for column in row:
            if isinstance(column, cx_Oracle.LOB):
                content_list.append(str(column))
            else:
                content_list.append(column)
        content = "".join(content_list)
        result_list.append(content)
    return result_list

        
#函数-获取住院号为patient_id的患者的出院证 嘉和系统存储电子病历时用的编码是cp936 本程序需要转换为utf-8才能处理
def get_discharge_certificate(item, cursor):
    
    #如果使用出院证作为抓取对象
    if G_use_discharge_certification:
        sql = "select file_no from jhmr_file_index where patient_id = '%s' and topic like '%%出院证%%'" % item.patient_id
    else:
        #顺产取分娩记录
        if item.delivery_mode == "1":
            sql = "select file_no from jhmr_file_index where patient_id = '%s' and topic like '%%分娩记录%%'" % item.patient_id
        #剖宫产取术后首次病程记录
        elif item.delivery_mode == "2":
            sql = "select file_no from jhmr_file_index where patient_id = '%s' and topic like '%%术后首次病程记录%%'" % item.patient_id
            
    cursor.execute(sql)
    result = cursor.fetchall()
    d_c_list = []
    
    for row in result:
    # 嘉和用文件ID定位特定的病历文件 文件ID编码规则如下
        file_uniq_no = "45038458-2-%s-2-1-0-%s" %(item.patient_id, str(row[0]))
        sql = "select d.mr_content from jhmr_file_content_TEXT d where d.file_unique_id = '%s'" % file_uniq_no
        cursor.execute(sql)
        inner_result = get_content_from_lob(cursor)
        for inner_row in inner_result:
            if len(inner_row) < 3:
                continue
            inner_row = inner_row.replace("\r\n","")
            inner_row = inner_row.replace(" ", "")
            inner_row = inner_row.decode('cp936').encode('utf-8')
            inner_row = inner_row.replace("：", ":")
            inner_row = inner_row.replace("一分钟", "1分钟")
            inner_row = inner_row.replace("急诊", "")
            inner_row = inner_row.replace("、", "")
            inner_row = inner_row.replace("，", "")
            inner_row = inner_row.replace("。", "")
            inner_row = inner_row.replace("“", "")
            inner_row = inner_row.replace("”", "")
            d_c_list.append(inner_row)
    return d_c_list


#处理日期字符串中的非数字字符
def remove_illegal_date(date_str):
    temp_str = date_str
    for index in range(len(temp_str)):
        if temp_str[index].isdigit():
            continue
        else:
            date_str = date_str.replace(temp_str[index], "")
    return date_str


#函数-处理分娩日期串的函数
def DOB_process(dob_str):
    if dob_str == "":
        return ""
    #过滤掉正则表达式匹配出来的无关汉字
    dob_str = dob_str.replace("于","")
    dob_str = dob_str.replace("予","")
    dob_str = dob_str.replace("在","")
    dob_str = dob_str.replace("行","")
    dob_str = dob_str.replace("因","")
    dob_str = dob_str.replace("顺","")
    dob_str = dob_str.replace("经","")
    dob_str = dob_str.replace("年","-")
    dob_str = dob_str.replace("月","-")
    dob_str = dob_str.replace("日","")
    dob_str = dob_str.replace("患者","")
    
    #处理2016-12-2518:20这样的时间串 按:分割取前面的部分进行处理
    if dob_str.find(":") != -1:
        temp_list = dob_str.split(':')
        dob_str = temp_list[0]
        dob_str = dob_str[:-2]
    
    #处理类似2016-12-25和12-25这样日期串 将其转换为20161225和1225 后者需要搭配入院日期处理
    count = dob_str.count('-')
    if count != 0:
        temp_dob_str = ""
        temp_list = dob_str.split('-')
        
        if count == 2:
            temp_list[0] = remove_illegal_date(temp_list[0])
            temp_list[1] = remove_illegal_date(temp_list[1])
            temp_list[2] = remove_illegal_date(temp_list[2])
            if len(temp_list[1]) == 1:
                temp_list[1] = "0" + temp_list[1]
            if len(temp_list[2]) == 1:
                temp_list[2] = "0" + temp_list[2]
        elif count == 1:
            temp_list[0] = remove_illegal_date(temp_list[0])
            temp_list[1] = remove_illegal_date(temp_list[1])
            if len(temp_list[0]) == 1:
                temp_list[0] = "0" + temp_list[0]
            if len(temp_list[1]) == 1:
                temp_list[1] = "0" + temp_list[1]
        dob_str = "".join(temp_list)
    return dob_str
    

#函数-处理新生儿apgar评分字符串
def apgar_process(apgar_str):
    if apgar_str == "":
        return ""
    if apgar_str == "满分":
        apgar_str = "10"
    else:
        apgar_searcher = re.compile(r'\d{1,2}分$')
        result = apgar_searcher.findall(apgar_str)
        if len(result) < 1:
            return ""
        apgar_str = result[0]
        apgar_str = apgar_str.replace("分","")
    return apgar_str
    

#函数-载入地址编码 地址字典结构为地名+数字编码 将常用的重庆 四川 贵州 以及全国和省份字典写在了代码里 以提高效率
def load_address_dict(file_name):
    dict_path = (G_path_prefix + r"puerpera_data_report\dict\division_dict" + "\\" + file_name + ".txt" ).decode('utf-8').encode('cp936')
    temp_dict = {}
    
    write_log(dict_path, "debug")
    
    dict_file = open(dict_path)
    if file_name == "全国":
        for line in dict_file:
            line = line.strip()
            if line == "" or line == "!@!":
                continue
            split_list = line.split(",")
            temp_dict[split_list[0]] = split_list[1]
    else:
        for line in dict_file:
            line = line.strip()
            if line == "":
                continue
            split_list = line.split(",")
            temp_dict[split_list[1]] = split_list[0]
    dict_file.close()
    
    if file_name == "重庆":
        G_dictionary.address_dict_chongqing = temp_dict
    elif file_name == "四川":
        G_dictionary.address_dict_sichuan = temp_dict
    elif file_name == "省份字典":
        G_dictionary.address_dict_allprovince = temp_dict
    elif file_name == "贵州":
        G_dictionary.address_dict_guizhou = temp_dict
    elif file_name == "全国":
        G_dictionary.address_dict_country = temp_dict
    else:
        G_dictionary.address_dict_other = temp_dict
    

#函数-载入通用字典 可载入民族和国家名称字典
def load_dict(file_name):
    dict_path = (G_path_prefix + r"puerpera_data_report\dict\\" + file_name + ".txt").decode('utf-8').encode('cp936')
    write_log(dict_path, "debug")
    temp_dict = {}
    
    dict_file = open(dict_path)
    for line in dict_file:
        line = line.strip()
        if line == "":
            continue
        split_list = line.split(",")
        if len(split_list) < 2:
            continue
        temp_dict[split_list[0]] = split_list[1]
    dict_file.close()
    
    if file_name == "country_dict":
        G_dictionary.country_name_dict = temp_dict
    elif file_name == "nation_dict":
        G_dictionary.nation_dict = temp_dict
    

#函数-判断输入行政区划编码的级别 3为省级 2为市级 1为区县级 不属于上述编码的返回0
def get_code_level(str):
    if str == "":
        return 0
    if len(G_level_searcher.searcher_province.findall(str)) > 0:
        return 3
    elif len(G_level_searcher.searcher_city.findall(str)) > 0:
        return 2
    elif len(G_level_searcher.searcher_county.findall(str)) > 0:
        return 1
    else:
        return 0


#函数-从地址字典中查询相应编码 输入参数为经过分词的地址串列表 调用此函数前应载入重庆 四川 贵州 省份字典
def get_code_from_dict(address_list):
    result_list = []
    #值为1时从地址列表的第二个元素进行判断 用于应对 沙坪坝区小龙坎街道 这样的地址
    omit_flag = 1
    dict_name = ""
    temp_dict = {}
    
    #输入参数合法性判断
    if len(address_list) == 0:
        write_log("地址字典为空","debug")
    
    write_log(convert("/ ".join(address_list)), "debug")
        
    #获取需要载入的字典名称 默认传入list的首元素应该为省份 先转为utf-8编码
    dict_name = address_list[0].encode('utf-8')
    write_log(convert("列表首元素:" + dict_name),"debug")
    
    #utf-8编码一个汉字需要3位 如果首元素的长度小于3说明不是一个汉字 明显这样是不合法的 默认返回重庆
    if len(dict_name) < 3:
        write_log(convert("省份地址不合法"),"debug")
        return result_list
    elif dict_name.count("省") != 0:
        dict_name = dict_name.replace("省","")
    elif dict_name.count("市") != 0:
        dict_name = dict_name.replace("市","")
        
    #先查找是否存在此省份 若查到先向结果列表中写入该省份编码
    if G_dictionary.address_dict_allprovince.has_key(dict_name):
        write_log(convert("应选取的字典名称为:" + dict_name),"debug")
        result_list.append(G_dictionary.address_dict_allprovince[dict_name])
    else:
        #若查不到 认为是重庆市内的地址 写入重庆市的编码并试图查询重庆市内的代码  后返回
        #如果已经选择了重庆字典 不再重复写入重庆编码
        if len(result_list) < 1:
            result_list.append("500000")
            omit_flag = 0
            temp_dict = G_dictionary.address_dict_chongqing
        #if G_dictionary.address_dict_chongqing.has_key(dict_name):
        #    result_list.append(G_dictionary.address_dict_chongqing[dict_name])
        #    return result_list
    
    #载入相应省份的字典 继续进行查找
    if dict_name == "重庆":
        temp_dict = G_dictionary.address_dict_chongqing
    elif dict_name == "四川":
        temp_dict = G_dictionary.address_dict_sichuan
    elif dict_name == "贵州":
        temp_dict = G_dictionary.address_dict_guizhou
    elif len(temp_dict) == 0:
        load_address_dict(dict_name)
        temp_dict = G_dictionary.address_dict_other
    
    for index in range(len(address_list)):
        #如果地址列表中只有一个元素 且不是省份名称 如只有一个巴南区 还是需要从第一个元素进行判断
        if index == 0 and omit_flag == 1 :
            continue
        #先转为utf-8编码
        item = address_list[index].encode('utf-8')
        write_log(convert("组内元素:" + item),"debug")
        #不处理长度小于4的
        if len(item) < 4:
            write_log("wrong element: " + convert(item) , "debug")
            continue
        #找到相应编码 写回结果列表
        if temp_dict.has_key(item):
            #如果结果列表中没有数据 则直接插入
            if len(result_list) < 1:
                result_list.append(temp_dict[item])
            #若结果列表中有数据 还应比较新取得的代码与表中最后一个元素的等级关系 默认由大到小插入列表 同级代码不应再继续插入
            else:
                if get_code_level(result_list[-1]) > get_code_level(temp_dict[item]):
                    result_list.append(temp_dict[item])

    return result_list

#写入结果excel的第一行
def write_excel_firstline(sheet):
    sheet.write(0, 0, convert_c("USERNAME"))    #用户名 填产妇姓名
    sheet.write(0, 1, convert_c("JG_ZC"))       #是否助产机构 一般填1 文本
    sheet.write(0, 2, convert_c("CF_XM"))       #产妇姓名
    sheet.write(0, 3, convert_c("CF_BAH"))      #产妇病案号 文本
    sheet.write(0, 4, convert_c("CF_ZJLX"))     #产妇证件类型 文本
    sheet.write(0, 5, convert_c("CF_ZJHM"))     #产妇证件号码 文本
    sheet.write(0, 6, convert_c("CF_CSRQ"))     #产妇出生日期 文本YYYYDDMM
    sheet.write(0, 7, convert_c("CF_GJ"))       #产妇国籍
    sheet.write(0, 8, convert_c("CF_MZ"))       #产妇民族 文本
    sheet.write(0, 9, convert_c("CF_HJ_S"))     #产妇户籍-省
    sheet.write(0, 10, convert_c("CF_HJ_SD"))    #产妇户籍-市
    sheet.write(0, 11, convert_c("CF_HJ_XQ"))    #产妇户籍-区县
    sheet.write(0, 12, convert_c("CF_HJ_QHDM"))  #产妇户籍-省-编码 文本
    sheet.write(0, 13, convert_c("CF_JZD_S"))    #产妇居住地-省
    sheet.write(0, 14, convert_c("CF_JZD_SD"))   #产妇居住地-市
    sheet.write(0, 15, convert_c("CF_JZD_XQ"))   #产妇居住地-区县
    sheet.write(0, 16, convert_c("CF_JZ_QHDM"))  #产妇居住地-省-编码 文本
    sheet.write(0, 17, convert_c("CF_YC"))       #产妇孕次 数字
    sheet.write(0, 18, convert_c("CF_CC"))       #产妇产次 数字
    sheet.write(0, 19, convert_c("CF_YFZC"))     #产妇孕周 数字
    sheet.write(0, 20, convert_c("CF_GWYS"))     #是否高危产妇 文本
    sheet.write(0, 21, convert_c("CF_FMDD"))     #分娩地点 填医疗机构内 1 文本
    sheet.write(0, 22, convert_c("CF_FMFS"))     #分娩方式 文本
    sheet.write(0, 23, convert_c("CF_FMRQ"))     #分娩日期 文本YYYYDDMM
    sheet.write(0, 24, convert_c("FM_XB1"))      #第一胎性别 文本
    sheet.write(0, 25, convert_c("FM_RSJJ1"))    #第一胎分娩结局
    sheet.write(0, 26, convert_c("FM_PF1"))      #第一胎apgar评分 数字
    sheet.write(0, 27, convert_c("FM_XB2"))      #第二胎性别 文本
    sheet.write(0, 28, convert_c("FM_RSJJ2"))    #第二胎分娩结局
    sheet.write(0, 29, convert_c("FM_PF2"))      #第二胎apgar评分 数字
    sheet.write(0, 30, convert_c("FM_XB3"))      #第三胎性别 文本
    sheet.write(0, 31, convert_c("FM_RSJJ3"))    #第三胎分娩结局
    sheet.write(0, 32, convert_c("FM_PF3"))      #第三胎apgar评分 数字
    sheet.write(0, 33, convert_c("FM_XB4"))      #第四胎性别 文本
    sheet.write(0, 34, convert_c("FM_RSJJ4"))    #第四胎分娩结局
    sheet.write(0, 35, convert_c("FM_PF4"))      #第四胎apgar评分 数字
    sheet.write(0, 36, convert_c("JG_DWFZR"))    #单位负责人 填左国庆
    sheet.write(0, 37, convert_c("JG_TBR"))      #填表人 任亚利 倪锐
    sheet.write(0, 38, convert_c("JG_LXDH"))     #联系电话 67063722 或 67983687
    sheet.write(0, 39, convert_c("JG_BCRQ"))     #报出日期
    
    return sheet
    
#函数-将抓取结果写入excel文件
def write_xls(info_list):
    if len(info_list) < 1:
        return
    try:
        result_xls = xlwt.Workbook(encoding='cp936')
        sheet = result_xls.add_sheet('sheet 1', cell_overwrite_ok = True)
    #写入首行
        sheet = write_excel_firstline(sheet)
    #行索引置为1
        line_index = 1
    
        today = datetime.date.today()
        date_str = today.strftime("%Y%m%d")

        for item in info_list:
            sheet.write(line_index, 0, convert_c("重庆市中医院"))
            sheet.write(line_index, 1, convert_c("1"))
            sheet.write(line_index, 2, convert_c(item.name))
            sheet.write(line_index, 3, item.patient_id)
            sheet.write(line_index, 4, item.id_type)
            sheet.write(line_index, 5, item.id_value)
            sheet.write(line_index, 6, item.date_of_birth)
            sheet.write(line_index, 7, convert_c(item.nation))
            sheet.write(line_index, 8, convert_c(item.ethnicity))
            sheet.write(line_index, 9, convert_c(item.registed_address_p))
            sheet.write(line_index, 10, convert_c(item.registed_address_ci))
            sheet.write(line_index, 11, convert_c(item.registed_address_co))
            sheet.write(line_index, 12, item.registed_address_code)
            sheet.write(line_index, 13, convert_c(item.domicile_p))
            sheet.write(line_index, 14, convert_c(item.domicile_ci))
            sheet.write(line_index, 15, convert_c(item.domicile_co))
            sheet.write(line_index, 16, convert_c(item.domicile_code))
            sheet.write(line_index, 17, item.gravidity)
            sheet.write(line_index, 18, item.parity)
            sheet.write(line_index, 19, item.gestational_weeks)
            sheet.write(line_index, 20, item.is_high_risk)
            sheet.write(line_index, 21, "1")
            sheet.write(line_index, 22, item.delivery_mode)
            sheet.write(line_index, 23, item.delivery_date)
            sheet.write(line_index, 24, item.fetus1_gender)
            sheet.write(line_index, 25, item.fetus1_outcome)
            sheet.write(line_index, 26, item.fetus1_agpar)
            
            if item.is_twin:
                sheet.write(line_index, 27, item.fetus2_gender)
                sheet.write(line_index, 28, item.fetus2_outcome)
                sheet.write(line_index, 29, item.fetus2_agpar)
            else:
                sheet.write(line_index, 27, "")
                sheet.write(line_index, 28, "")
                sheet.write(line_index, 29, "")
                
            sheet.write(line_index, 30, "")
            sheet.write(line_index, 31, "")
            sheet.write(line_index, 32, "")
            sheet.write(line_index, 33, "")
            sheet.write(line_index, 34, "")
            sheet.write(line_index, 35, "")
            sheet.write(line_index, 36, convert_c("左国庆"))
            sheet.write(line_index, 37, convert_c("任亚利"))
            sheet.write(line_index, 38, convert_c("67063722"))
            sheet.write(line_index, 39, convert_c(date_str))
            line_index = line_index + 1
    finally:    
        result_xls.save((G_path_prefix + r"puerpera_data_report\result_" + G_datestr_for_log + ".xls").decode('utf-8').encode('cp936'))
    
    
#函数-将抓取结果写入csv文件
def write_csv(excel_file, item):
    excel_file.write(convert_c(item.name) + ",")
    excel_file.write(convert_c(item.patient_id) + ",")
    excel_file.write(convert_c(item.diagnosis) + ",")
    
    if item.is_twin == True:
        excel_file.write(convert_c("双胞胎") + ",")
    else:
        excel_file.write(convert_c("单胎") + ",")
    if item.delivery_mode == "1":
        excel_file.write(convert_c("阴道产") + ",")
    else:
        excel_file.write(convert_c("剖宫产") + ",")
    
    excel_file.write(convert_c(item.delivery_date) + ",")
    excel_file.write(convert_c(item.nation) + ",")
    excel_file.write(convert_c(item.ethnicity) + ",")
    excel_file.write(convert_c(item.id_type) + ",")
    excel_file.write(convert_c("'" + item.id_value) + ",")
    excel_file.write(convert_c(item.date_of_birth) + ",")
    excel_file.write(convert_c(str(item.gestational_weeks)) + ",")
    excel_file.write(convert_c(str(item.gravidity)) + ",")
    excel_file.write(convert_c(str(item.parity)) + ",")
    excel_file.write(convert_c(str(item.fetus1_agpar)) + ",")
    excel_file.write(convert_c(str(item.fetus2_agpar)) + ",")
    
    if item.fetus1_outcome == "1":
        excel_file.write(convert_c("第一胎活产") + ",")
    elif item.fetus1_outcome == "2":
        excel_file.write(convert_c("第一胎未存活") + ",")
        
    if item.fetus2_outcome == "1":
        excel_file.write(convert_c("第二胎活产") + ",")    
    elif item.fetus2_outcome == "2":
        excel_file.write(convert_c("第二胎未存活") + ",")
    else:
        excel_file.write(convert_c("未生育第二胎") + ",")
            
    if item.fetus1_gender == "1":
        excel_file.write(convert_c("第一胎性别: 男") + ",")    
    elif item.fetus1_gender == "2":
        excel_file.write(convert_c("第一胎性别: 女") + ",")    
    else:
        excel_file.write(convert_c("第一胎性别: 不明") + ",")
            
    if item.fetus2_gender == "1":
        excel_file.write(convert_c("第二胎性别: 男") + ",")    
    elif item.fetus2_gender == "2":
        excel_file.write(convert_c("第二胎性别: 女") + ",")
    else:
        excel_file.write(convert_c("第二胎性别: 不明") + ",")
    
    excel_file.write(convert_c(item.registed_address_p) + ",")
    excel_file.write(convert_c(item.registed_address_ci) + ",")
    excel_file.write(convert_c(item.registed_address_co) + ",")
    excel_file.write(convert_c(item.registed_address_code) + ",")
    
    excel_file.write(convert_c(item.domicile_p) + ",")
    excel_file.write(convert_c(item.domicile_ci) + ",")
    excel_file.write(convert_c(item.domicile_co) + ",")
    excel_file.write(convert_c(item.domicile_code))
    excel_file.write("\r")

#函数-将抓取结果写入文本文件
def write_text(file, item):
    file.write(convert("产妇姓名: " + item.name) + "/ ")
    file.write(convert("产妇病案号: " + item.patient_id) + "/ ")
    file.write(convert("出院诊断: " + item.diagnosis) + "/ ")
    
    if item.is_twin == True:
        file.write(convert("双胞胎") + "/ ")
    else:
        file.write(convert("单胎") + "/ ")
        
    if item.delivery_mode == "1":
        file.write(convert("阴道产") + "/ ")
    elif item.delivery_mode == "2":
        file.write(convert("剖宫产") + "/ ")
    
    file.write(convert("分娩日期: ") + item.delivery_date + "/ ")
    file.write(convert("产妇国籍: ") + item.nation + "/ ")
    file.write(convert("产妇民族编码: ") + item.ethnicity + "/ ")
    file.write(convert("证件类型: ") + item.id_type + "/ " )
    file.write(convert("身份证号: ") + item.id_value + "/ ")
    file.write(convert("产妇出生日期: ") + item.date_of_birth + "/ ")    
    file.write(convert("产妇孕周: ") + str(item.gestational_weeks) + "/ ")
    file.write(convert("孕次: " + str(item.gravidity) + " 产次: " + str(item.parity)) + "/ ")    
    file.write(convert("第一胎apgar评分: ") + item.fetus1_agpar +  "/ ")        
    file.write(convert("第二胎apgar评分: ") + item.fetus2_agpar +  "/ ")
    
    if item.fetus1_outcome == "1":
        file.write(convert("第一胎活产") + "/ ")
    elif item.fetus1_outcome == "2":
        file.write(convert("第一胎未存活") + "/ ")
        
    if item.fetus2_outcome == "1":
        file.write(convert("第二胎活产") + "/ ")
    elif item.fetus2_outcome == "2":
        file.write(convert("第二胎未存活") +   "/ ")
    else:
        file.write(convert("未生育第二胎") +   "/ ")
        
    if item.fetus1_gender == "1":
        file.write(convert("第一胎性别: 男") + "/ ")
    elif item.fetus1_gender == "2":
        file.write(convert("第一胎性别: 女") + "/ ")
    else:
        file.write(convert("第一胎性别: 不明") + "/ ")
        
    if item.fetus2_gender == "1":
        file.write(convert("第二胎性别: 男") + "/ ")
    elif item.fetus2_gender == "2":
        file.write(convert("第二胎性别: 女") + "/ ")
    else:
        file.write(convert("第二胎性别: 不明") + "/ ")
    
    file.write(convert("户籍地址: ") + convert(item.registed_address_p + " " + item.registed_address_ci + " " + item.registed_address_co + " " + item.registed_address_code) + "/ ")
    file.write(convert("居住地: ") + convert(item.domicile_p + " " + item.domicile_ci + " " + item.domicile_co + " " + item.domicile_code) +   "/ ")
    file.write("\r")    

# 接受三种形式的输入
#无参数 提取昨天一天的数据
#单参数 数字x 即提取x天前到今天（不包括今天）的数据
#双参数 起始日期 结束日期 提取起止日期间的数据（不包括结束日期当天）
if __name__ == '__main__':
    conn = None
    #无参数的情况
    if len(sys.argv) == 1:
        end_str = datetime.date.today().strftime("%Y/%m/%d")
        begin_str = (datetime.date.today() - datetime.timedelta(days = 1)).strftime("%Y/%m/%d")
    #单参数的情况
    elif len(sys.argv) == 2:
        days = sys.argv[1].strip()
        if not days.isdigit():
            print convert("输入参数不合法 应输入数字")
            sys.exit()
        end_str = datetime.date.today().strftime("%Y/%m/%d")
        begin_str = (datetime.date.today() - datetime.timedelta(days = int(days))).strftime("%Y/%m/%d")
    #双参数的情况
    elif len(sys.argv) == 3:
        arg_checker = re.compile(r'\d{4}/\d{2}/\d{2}')
        if len(arg_checker.findall(sys.argv[1])) < 1 or len(arg_checker.findall(sys.argv[2])) < 1:
            print convert("输入参数不合法 形为YYYY/MM/DD的日期")
            sys.exit()
        begin_str = sys.argv[1]
        end_str = sys.argv[2]
    else:
        print convert("输入参数不合法 应输入数字")
        sys.exit()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        get_basic_info(cursor, begin_str, end_str)
        build_info(cursor)
    finally:
        if conn:
            close_connection(conn)
    
    #写文本文件
    #file = open(r"F:\puerpera_data_report\result.txt".decode('utf-8').encode('cp936'), "a+")
    #写csv文件
    #excel_file = open(r"F:\puerpera_data_report\result.csv".decode('utf-8').encode('cp936'), "a+")
    
    print convert("G_info_list数组长度: ") + str(len(G_info_list))
        
    #for item in G_info_list:
        #write_text(file,item)
        #write_csv(excel_file, item)
        
    write_xls(G_info_list)
    #file.close()
    #excel_file.close()
