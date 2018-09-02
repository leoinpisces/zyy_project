#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import jieba
import xlwt
import xlrd
import datetime
import logging
import logging.handlers
import db_connector

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')


G_CQ_old_code = {"510202":"渝中区", "510203":"大渡口区", "510211":"江北区", "510212":"沙坪坝区", "510213":"九龙坡区", 
                 "510214":"南岸区", "510215":"北碚区", "510216":"万盛区", "510217":"大足区", "510218":"渝北区", 
                 "510219":"巴南区", "510221":"长寿区", "510222":"巴南区", "510223":"綦江区", "510224":"渝北区", 
                 "510225":"江津区", "510226":"合川区", "510227":"潼南区", "510228":"铜梁区", "510229":"永川区", 
                 "510230":"大足区", "510231":"北碚区", "510232":"璧山区", "511202":"万州区", "511203":"万州区", 
                 "511204":"万州区", "511211":"开州区", "511222":"忠县", "511223":"梁平区", "511224":"云阳县", 
                 "511225":"奉节县", "511226":"巫山县", "511227":"巫溪县", "511228":"城口县", "513521":"石柱土家族自治县", 
                 "513522":"秀山土家族苗族自治县", "513523":"黔江区", "513524":"酉阳土家族苗族自治县", "512301":"涪陵区", 
                 "512324":"丰都县", "512301":"涪陵区", "512322":"垫江县", "512323":"南川区", "512326":"武隆县", "512225":"云阳县", 
                 "512223":"忠县", "512229":"城口县"}

#需要从地址串中删除的字符串样式表
G_trush_str_list = ["省市县（区）", "县（区）", "个体参保虚拟单位", "省市县",  "省市", "/", "灵活就业人员", 
                    "（具体不详）", "同现住地址", "具体不详", "不详", "大龄下岗退休职工虚拟单位", "（临时聘用人员）", "(临聘人员)"]
#需要利用正则表达式从地址串中删除的 
G_trush_patten = r'-$|^-|^省|/$|^=-|无$'
#需要在地址串中替换的 结构为 {"需替换的字符串","替换后的字符串"}
G_replace_dict = {"市市":"市", "市县":"市", "区县":"区", "县县":"县", "区区":"区", "区(县)":"区"}
#省级行政区划编码匹配正则表达式
G_province_re = re.compile(r'[1-9]\d0{4}')
#市级行政区划编码匹配正则表达式
G_city_re = re.compile(r'\d{2}[1-9]\d00|\d{2}\d[1-9]00')
#区县级行政区划编码匹配正则表达式
G_county_re = re.compile(r'\d{4}[1-9]\d|\d{4}\d[1-9]')
#行政区划层级代码字典
G_district_level_code = {"province":3, "city":2, "country":1, "unknown":0}

#生成日志记录对象
G_logger = logging.getLogger('season_report_logger')

#相关文件路径
G_path_prefix = r"E:\project\season_report_fix"

#初始化日志记录对象
def init_logger():
    #引用全局变量
    global G_logger
    
    #日志文件名称
    datestr_for_log = datetime.date.today().strftime("%Y-%m-%d")
    
    #获取日志文件所在路径
    if os.path.exists(r"D:\\".decode('utf-8').encode('cp936')):
        log_file_path = (r"D:\season_report_fix_log\%s\\" % datestr_for_log).decode('utf-8').encode('cp936')
    else:
        log_file_path = (r"C:\season_report_fix_log\%s\\" % datestr_for_log).decode('utf-8').encode('cp936')
        
    #如果日志路径不存在 就需要创建一个
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)
        
    #设置日志文件路径
    log_file = log_file_path + (r"fix_log_%s.log" % datestr_for_log).decode('utf-8').encode('cp936')
    
    #日志文件handler 用于日志文件分割  按文件大小分割日志 单个日志文件大小为10M
    log_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes = 10240*1024, backupCount = 100)
    
    #日志格式
    formatter = logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    
    #添加文件处理器
    G_logger.addHandler(log_handler)
    #设置日志记录级别
    G_logger.setLevel(logging.DEBUG)

#调用函数 初始化日志记录器
init_logger()

#函数-转换为中文操作系统可读的编码
def convert_c(text_str):
    return text_str.decode('utf-8').encode('cp936')

#季报中患者基本信息的类
class patient_info:
    name = ""  #患者姓名
    ID_Num = "" #患者身份证号
    patient_id = "" #患者病案号
    
    domicile = "" #患者现住址
    domicile_res = "" #处理过的患者现住址
    
    birth_place = "" #患者出生地
    birth_place_res = "" #处理过的患者出生地
    
    registed_addr = "" #患者户口地址
    registed_addr_res = "" #处理过的患者户口地址
    
    native_place = "" #患者籍贯
    native_place_res = "" #处理过的患者籍贯

def get_last_month():
    today = datetime.date.today()
    this_year = today.year
    this_month = today.month
    #取上一个月
    if this_month == 1:
        this_month = 12
        this_year -= 1
    else:
        this_month -= 1
    
    temp_date = datetime.date(this_year, this_month, today.day)
    return temp_date.strftime('%Y%m')

class address_processor():
    #构造函数
    def __init__(self):
        #去除垃圾字符串的正则表达式列表
        self.trush_remove_re = re.compile(G_trush_patten)
        #全国所有地区的字典
        self.all_dict = self.load_dict("全国")
        #所有省份字典
        self.province_dict = self.load_dict("省份字典")
        #重庆字典
        self.ChongQing_dict = self.load_dict("重庆")
        #其他字典
        self.addr_dict = {}
        
        if self.all_dict == None or self.ChongQing_dict == None or self.province_dict == None:
            G_logger.error(convert_c("地址串处理器初始化失败"))
            sys.exit()
        else:
            G_logger.debug( convert_c("地址串处理器初始化成功") )
            
        jieba.load_userdict((G_path_prefix + r"\dict\district_dict.txt").decode('utf-8').encode('cp936'))
        
    def load_dict(self, dict_name):
        dict_path = (G_path_prefix + r"\dict\division_dict" + "\\" + dict_name + ".txt" ).decode('utf-8').encode('cp936')
        temp_dict = {}
        
        try:
            dict_file = open(dict_path)
            #全国字典是类似{编码,名称}形式的载入系统的
            if dict_name == "全国":
                for line in dict_file:
                    line = line.strip()
                    if line == "" or line == "!@!" or line.count("#") != 0:
                        continue
                    split_list = line.split(",")
                    temp_dict[split_list[0]] = split_list[1]
            else:
                for line in dict_file:
                    line = line.strip()
                    if line == "" or line == "!@!" or line.count("#") != 0:
                        continue
                    split_list = line.split(",")
                    temp_dict[split_list[1]] = split_list[0]
            dict_file.close()
            return temp_dict
        except IOError:
            G_logger.error(convert_c("地址字典-%s载入失败" % dict_name))
            return None
        
    #过滤一些固定模式的垃圾字符串
    def addr_mode_process(self, addr_str):
        addr_str = str(addr_str).strip()
        #去掉字符串前后的字符
        addr_str = addr_str.strip()
        if len(addr_str) == 0:
            return addr_str
        #通过简单匹配 删除已定字符串 
        for trash_str in G_trush_str_list:
            if trash_str in addr_str:
                addr_str = addr_str.replace(trash_str, "")
        #通过正则表达式组 删除已定字符串
        addr_str = self.trush_remove_re.sub('', addr_str)
        #简单替换字符串
        for key in G_replace_dict.keys():
            if key in addr_str:
                addr_str = addr_str.replace(key, G_replace_dict[key])
        
        #返回处理结果
        return addr_str
    
    #获取行政区划编码级别
    def get_district_level(self, code_str):
        if len(G_province_re.findall(code_str)) > 0:
            return G_district_level_code["province"]
        elif len(G_city_re.findall(code_str)) > 0:
            return G_district_level_code["city"]
        elif len(G_county_re.findall(code_str)) > 0:
            return G_district_level_code["country"]
        else:
            return G_district_level_code["unknown"]
    
    #根据行政区划字典对地址字符串进行处理
    def addr_dict_process(self, addr_str):
        if len(addr_str) == 0:
            return addr_str
        
        addr_str = addr_str.encode('utf-8', 'ignore')
        #地址匹配字典置空
        self.addr_dict = {}
        
        temp_list = list( jieba.cut(addr_str, cut_all = False) )
        seg_list = list( set(temp_list) )
        seg_list.sort(key=temp_list.index)
        G_logger.debug( convert_c( "\n处理前地址串为\n---%s---\n分词结果为\n---%s---" % ( addr_str, "-".join(seg_list) ) ) )
        
        #暂存以匹配出来的地址
        temp_district_dict = {}
        
        #结构化地址与非结构化地址的分界点
        divide_index = -1
        
        #结果串
        result_str = ""
        
        #切分列表默认的顺序是从省级地址到区县级地址的 
        for seg_str in seg_list:
            #长度不足2地址串的不作为筛选对象
            if len(seg_str) < 2 or seg_str.isdigit():
                continue
            
            #字典是utf-8编码的 所有需要先进行转码
            seg_str = seg_str.encode('utf-8', 'ignore')
            
            #先判断省级字典 如果在省份字典中查找到了相应省 且 层级字典中没有省级区划  就要先查询省级字典
            if self.province_dict.has_key(seg_str):
                if not temp_district_dict.has_key("province"):
                    temp_district_dict["province"] = self.all_dict[self.province_dict[seg_str]]
                elif self.province_dict[seg_str] == self.province_dict[temp_district_dict["province"]]:
                    divide_index = addr_str.rfind(seg_str) + len(seg_str)
                #判断是否重庆的地址
                if seg_str.count("重庆") != 0:
                    self.addr_dict = self.ChongQing_dict
                else:
                    self.addr_dict = self.load_dict(seg_str)
            #非省级地址的情况
            elif len(self.addr_dict) != 0:
                if self.addr_dict.has_key(seg_str):
                    temp_code = self.addr_dict[seg_str]
                    #如果为市级地址 判断是否已经有市级地址 若无 需要添加
                    if self.get_district_level(temp_code) == G_district_level_code["city"]:
                        if not temp_district_dict.has_key("city"):
                            temp_district_dict["city"] = self.all_dict[self.addr_dict[seg_str]]
                            divide_index = addr_str.rfind(seg_str) + len(seg_str)
                        else:
                            divide_index = addr_str.rfind(seg_str) + len(seg_str)
                    #如果为区县级地址
                    elif self.get_district_level(temp_code) == G_district_level_code["country"]:
                        if not temp_district_dict.has_key("country"):
                            temp_district_dict["country"] = self.all_dict[self.addr_dict[seg_str]]
                            divide_index = addr_str.rfind(seg_str) + len(seg_str)
                            #如果有区县级地址而无市级地址 还需倒推市级地址
                            if not temp_district_dict.has_key("city") and temp_district_dict["province"].count("北京") == 0 \
                            and temp_district_dict["province"].count("上海") == 0 and temp_district_dict["province"].count("天津") == 0 \
                            and temp_district_dict["province"].count("重庆") == 0:
                                city_code = temp_code[0:4] + "00"
                                temp_district_dict["city"] = self.all_dict[city_code]
                        else:
                            divide_index = addr_str.rfind(seg_str) + len(seg_str)
            
            #如果不是上述情况 尝试在重庆字典中查找
            elif self.ChongQing_dict.has_key(seg_str):
                temp_district_dict["city"] = "重庆市"
                temp_district_dict["country"] = self.all_dict[self.ChongQing_dict[seg_str]]
                divide_index = addr_str.rfind(seg_str) + len(seg_str)
        
        #拼接地址串                   
        if temp_district_dict.has_key("province"):
            result_str = result_str + temp_district_dict["province"]
        if temp_district_dict.has_key("city") and temp_district_dict["city"] != "市辖区" \
        and temp_district_dict["city"] != "省直辖县级行政区划":
            result_str = result_str + temp_district_dict["city"]
        if temp_district_dict.has_key("country"):
            result_str =  result_str + temp_district_dict["country"]
        if divide_index != -1:
            result_str = result_str + addr_str[divide_index:]
            
        G_logger.debug(convert_c("通过分词确定的地址字符串为\n---%s---" % result_str))
            
        return self.addr_mode_process(result_str)
    
    def get_addr_ID(self, ID_num):
        #先判断身份证号长度是否符合要求
        if len(ID_num) != 15 and len(ID_num) != 18:
            G_logger.error(convert_c("身份证号-%s-有误" % ID_num))
            return ""
        district_code = ID_num[:6]
        country = ""
        city = ""
        province = ""
        #根据行政区划编码确定地址名称
        if self.all_dict.has_key(district_code):
            country = self.all_dict[district_code]
            if district_code[:3] == "500":
                city = "重庆市"
            elif district_code[:3] == "110":
                city = "北京市"
            elif district_code[:3] == "120":
                city = "天津市"
            elif district_code[:3] == "310":
                city = "上海市"
            else:
                city = self.all_dict[district_code[:4] + "00"]
                province = self.all_dict[district_code[:2] + "0000"]
        #重庆直辖前的地址编码
        elif G_CQ_old_code.has_key(district_code):
            country = G_CQ_old_code[district_code]
            province = "重庆市"
        
        if city != "市辖区" and city != "省直辖县级行政区划":
            result_str = province + city + country
        else:
            result_str = province + country
        G_logger.debug(convert_c("由身份证号获取到地址为---%s" % result_str))
        return result_str
    
    #从数据库中获取数据  
    def get_info_fromDB(self, date_str = get_last_month()):
        if len(date_str) < 5 and date_str != 'ALL':
            return None
        conn = db_connector.db_connector(dsn = "DmkHis", usrname = "dhact", pwd = "dhact@SYS", db_type = "cache")
        if date_str == 'ALL':
            sql = "SELECT MRZYWT_bah, MRZYWT_sfzh, MRZYWT_csd, MRZYWT_gg, MRZYWT_hkdz, MRZYWT_xzz FROM dhcmrzywtfinfo"
        else:
            sql = "SELECT MRZYWT_bah, MRZYWT_sfzh, MRZYWT_csd, MRZYWT_gg, MRZYWT_hkdz, MRZYWT_xzz FROM dhcmrzywtfinfo WHERE MRZYWT_cysj LIKE '%s%%'" % date_str
        sql = sql.decode('utf-8')
        info_rows = conn.get_rows(sql)       
        G_logger.debug(convert_c("执行sql语句\n%s" % sql))
        
        info_list = []
        for info in info_rows:
            temp_patient = patient_info()
            temp_patient.patient_id = str(info[0]).strip()
            temp_patient.ID_Num = str(info[1]).strip()
            temp_patient.birth_place = str(info[2]).strip()
            temp_patient.native_place = str(info[3]).strip()
            temp_patient.registed_addr = str(info[4]).strip()
            temp_patient.domicile = str(info[5]).strip()
            info_list.append(temp_patient)
        
        return info_list
    
    #生成更新数据库的sql
    def gen_sql(self):
        #如果结果文件存在才进行导入
        res_path = (G_path_prefix + r'\sample\sample_result.xls').decode('utf-8').encode('cp936')
        sql_list = []
        if os.path.exists(res_path):
            try:
                #打开工作表
                workbook = xlrd.open_workbook(res_path)
                active_sheet = workbook.sheet_by_name('Sheet1')
                #第一行为表头 所以从第二行开始读取数据写入数据库
                for row_index in range(1, active_sheet.nrows):
                    #只有line_flag为R的行才需要进行处理
                    line_flag = active_sheet.cell(row_index, 0).value
                    line_flag = line_flag.encode('utf-8')
                    if line_flag == "O":
                        tmp_bah = (active_sheet.cell(row_index, 1).value).decode('cp936').encode('utf-8')
                        tmp_sfzh = (active_sheet.cell(row_index, 2).value).decode('cp936').encode('utf-8')
                    elif line_flag == 'R':
                        tmp_csd = str(active_sheet.cell(row_index, 3).value)
                        #tmp_csd = tmp_csd.decode('cp936').encode('utf-8')
                        
                        tmp_gg = str(active_sheet.cell(row_index, 4).value)
                        #tmp_gg = tmp_gg.decode('cp936').encode('utf-8')
                        
                        tmp_hkdz = str(active_sheet.cell(row_index, 5).value)
                        #tmp_hkdz = tmp_hkdz.decode('cp936').encode('utf-8')
                        
                        tmp_xzz = str(active_sheet.cell(row_index, 6).value)
                        #tmp_xzz = tmp_xzz.decode('cp936').encode('utf-8')
                        
                        tmp_sql = "update dhcmrzywtfinfo set MRZYWT_csd = '%s', MRZYWT_gg = '%s', MRZYWT_hkdz = '%s', MRZYWT_xzz = '%s' where MRZYWT_bah = '%s' and MRZYWT_sfzh = '%s'" % (tmp_csd, tmp_gg, tmp_hkdz, tmp_xzz, tmp_bah, tmp_sfzh)
                        sql_list.append(tmp_sql)
                
                #返回生成的sql列表
                return sql_list
            except Exception, e:
                G_logger.error(convert_c("Excel读取失败!!原因为%s" % str(e)))
                return None
    
    #将验证过的数据写入数据库
    def upload_info_toDB(self):
        sql_list = self.gen_sql()
        if sql_list == None:
            G_logger.error(convert_c("sql列表无内容"))
            return None
        
        conn = db_connector.db_connector(dsn = "DmkHis", usrname = "dhact", pwd = "dhact@SYS", db_type = "cache")
        
        for sql in sql_list:
            sql = sql.decode('utf-8')
            excute_result = conn.excute_sql(sql)
            if type(excute_result) == type('error'):
                G_logger.error(convert_c("执行sql语句失败:\n%s\n错误信息为:\n%s" % (sql, excute_result) ))
            else:
                G_logger.debug(convert_c("执行sql语句成功:\n%s" % sql))
            #G_logger.debug(convert_c("执行sql语句成功:\n%s" % sql))
        
        print "Data uploaded"
            
            
    #从excel表格中获取数据
    def get_info_fromXL(self, path):
        info_list = []
        try:
            #打开工作表
            workbook = xlrd.open_workbook(path)
            #取活动sheet
            active_sheet = workbook.sheet_by_name('Sheet1')
            #取每一行的值 略过第一行表头
            for row_index in range(1, active_sheet.nrows):
                temp_patient = patient_info()
                #读取每行的信息
                temp_patient.patient_id = active_sheet.cell(row_index, 0).value
                temp_patient.ID_Num = active_sheet.cell(row_index, 1).value
                
                temp_patient.birth_place = active_sheet.cell(row_index, 2).value
                #temp_patient.birth_place = temp_patient.birth_place.decode('cp936').encode('utf-8')
                
                temp_patient.native_place = active_sheet.cell(row_index, 3).value
                #temp_patient.native_place = temp_patient.native_place.decode('cp936').encode('utf-8')
                
                temp_patient.registed_addr = active_sheet.cell(row_index, 4).value
                #temp_patient.registed_addr = temp_patient.registed_addr.decode('cp936').encode('utf-8')
                
                temp_patient.domicile = active_sheet.cell(row_index, 5).value
                #temp_patient.domicile = temp_patient.domicile.decode('cp936').encode('utf-8')
                
                #灌入info_list
                info_list.append(temp_patient)
            return info_list
                
        except:
            G_logger.error(convert_c("Excel读取失败!!"))
            return None
        
    def addr_main_process(self, date_str = get_last_month()):
        info_list = self.get_info_fromDB(date_str)
        if info_list == None:
            info_list = self.get_info_fromXL((G_path_prefix + r'\sample\info.xlsx').decode('utf-8').encode('cp936'))
        
        if info_list == None:
            G_logger.error(convert_c("获取患者信息失败"))
            return None
        
        sample_result = open( (G_path_prefix + r'\sample\sample_result.txt').decode('utf-8').encode('cp936'), 'a+' )
        for item in info_list:
            G_logger.debug(convert_c("病案号%s\n" % item.patient_id))
            #处理出生地
            G_logger.debug(convert_c("处理出生地\n"))
            G_logger.debug(convert_c("处理前的出生地为:%s\n" % item.birth_place))
            temp_line = self.addr_mode_process(item.birth_place)
            temp_line = self.addr_dict_process(temp_line)
            temp_line = temp_line.encode('utf-8', 'ignore')
            #utf-8 一个字长度为3 小于9个字符 就是小于三个字
            if len(temp_line) < 9:
                temp_line = self.get_addr_ID(item.ID_Num)
            item.birth_place_res = temp_line
            G_logger.debug(convert_c("处理后的出生地为:%s\n" % item.birth_place_res))
            
            #处理籍贯
            G_logger.debug(convert_c("处理籍贯\n"))
            G_logger.debug(convert_c("处理前的籍贯为%s\n" % item.native_place))
            temp_line = self.addr_mode_process(item.native_place)
            temp_line = self.addr_dict_process(temp_line)
            temp_line = temp_line.encode('utf-8', 'ignore')
            #utf-8 一个字长度为3 小于9个字符 就是小于三个字
            if len(temp_line) < 9:
                temp_line = self.get_addr_ID(item.ID_Num)
            item.native_place_res = temp_line
            G_logger.debug(convert_c("处理后的籍贯:%s\n" % item.native_place_res))
            
            #处理户口地址
            G_logger.debug(convert_c("处理户口地址\n"))
            G_logger.debug(convert_c("处理前的户口地址为%s\n" % item.registed_addr))
            temp_line = self.addr_mode_process(item.registed_addr)
            temp_line = self.addr_dict_process(temp_line)
            temp_line = temp_line.encode('utf-8', 'ignore')
            #utf-8 一个字长度为3 小于9个字符 就是小于三个字
            if len(temp_line) < 10:
                temp_line = self.get_addr_ID(item.ID_Num)
            item.registed_addr_res = temp_line
            G_logger.debug(convert_c("处理后的户口地址为:%s\n" % item.registed_addr_res))
            
            #处理现住址
            G_logger.debug(convert_c("处理现住址\n"))
            G_logger.debug(convert_c("处理前的现住址为%s\n" % item.domicile))
            temp_line = self.addr_mode_process(item.domicile)
            temp_line = self.addr_dict_process(temp_line)
            temp_line = temp_line.encode('utf-8', 'ignore')
            #utf-8 一个字长度为3 小于9个字符 就是小于三个字
            if len(temp_line) < 9:
                temp_line = self.get_addr_ID(item.ID_Num)
            item.domicile_res = temp_line
            G_logger.debug(convert_c("处理后现住址为:%s\n" % item.domicile_res))
            
            #如果没有取到相关地址 都取户口地址 如果户口地址也是空的 就取重庆市渝中区
            if item.registed_addr_res == "":
                item.registed_addr_res = "重庆市渝中区"
            
            if item.birth_place_res == "":
                item.birth_place_res = item.registed_addr_res
            
            if item.domicile_res == "":
                item.domicile_res = item.registed_addr_res
                
            if item.native_place_res == "":
                item.native_place_res = item.registed_addr_res
            
            sample_result.write("病案号:%s\n" % item.patient_id)
            sample_result.write("出生地为:%s\n" % item.birth_place_res)
            sample_result.write("籍贯为:%s\n" % item.native_place_res)
            sample_result.write("现住址为:%s\n" % item.domicile_res)
            sample_result.write("户口地址为:%s\n" % item.registed_addr_res)
            sample_result.write("\r\n")

        sample_result.close()
        return info_list
    
    #写入结果excel的第一行表头 表结构为 状态标志(E:空行 O:原数据 R:经过处理的数据) 病案号 身份证号 出生地  籍贯 户口地址  现住址 
    def write_xls_head(self, sheet):
        sheet.write(0, 0, convert_c("状态标志"))
        sheet.write(0, 1, convert_c("病案号"))
        sheet.write(0, 2, convert_c("身份证号"))
        sheet.write(0, 3, convert_c("出生地"))
        sheet.write(0, 4, convert_c("籍贯"))
        sheet.write(0, 5, convert_c("户口地址"))
        sheet.write(0, 6, convert_c("现住址"))
      
        
    #将结果写入excel 入参为处理结果list
    def write_res_xls(self, result_list):
        if result_list == None:
            return
        
        #写入excel
        try:
            result_xls = xlwt.Workbook(encoding='cp936')
            sheet = result_xls.add_sheet('Sheet1', cell_overwrite_ok = True)
            #写入表头
            self.write_xls_head(sheet)
            #行索引置1 从第一行开始写 第0行是表头
            line_index = 1
            
            #设置字体
            res_font = xlwt.Font()
            res_font.colour_index = 2
            res_font.bold = True
            
            res_style = xlwt.XFStyle()
            res_style.font = res_font
            
            for patient in result_list:
                #写入原数据
                sheet.write(line_index, 0, "O")
                sheet.write(line_index, 1, patient.patient_id)
                sheet.write(line_index, 2, patient.ID_Num)
                sheet.write(line_index, 3, convert_c(patient.birth_place))
                sheet.write(line_index, 4, convert_c(patient.native_place))
                sheet.write(line_index, 5, convert_c(patient.registed_addr))
                sheet.write(line_index, 6, convert_c(patient.domicile))
                line_index = line_index + 1
                
                #写入处理后数据
                sheet.write(line_index, 0, "R")
                sheet.write(line_index, 3, convert_c(patient.birth_place_res), res_style)
                sheet.write(line_index, 4, convert_c(patient.native_place_res), res_style)
                sheet.write(line_index, 5, convert_c(patient.registed_addr_res), res_style)
                sheet.write(line_index, 6, convert_c(patient.domicile_res), res_style)
                line_index = line_index + 1
                
                #写入空行
                sheet.write(line_index, 0, "E")
                for i in range(1, 7):
                    sheet.write(line_index, i, "")
                line_index = line_index + 1
        finally:
            result_xls.save((G_path_prefix + r'\sample\sample_result_' + datetime.date.today().strftime("%Y%m%d") + ".xls").decode('utf-8').encode('cp936'))

#测试函数 正式环境下不会使用  
def unit_test():
    str_processer = address_processor()
    sample_path =  (G_path_prefix + r'\sample\sample.txt').decode('utf-8').encode('cp936')
    sample_file = open(sample_path)
    sample_result = open( (G_path_prefix + r'\sample\sample_result.txt').decode('utf-8').encode('cp936'), 'a+' )
    for line in sample_file:
        temp_line = str_processer.addr_mode_process(line)
        temp_line = str_processer.addr_dict_process(temp_line)
        sample_result.write(line)
        sample_result.write(temp_line)
        sample_result.write("\r\n")  
    sample_result.close()
    sample_file.close()
    test_str = "省市县渝中区解放西路99号7-2-3"
    test_str = str_processer.addr_mode_process(test_str)
    test_str = str_processer.addr_dict_process(test_str)
    print test_str
    
if __name__ == '__main__':
    #输入参数有三种情况
    
    #构造处理器对象
    str_processer = address_processor()
    #情况1 输入参数为两个 分别为执行标志位 需要处理的月份
    if len(sys.argv) == 3:
        E_flag = sys.argv[1]
        month = str(sys.argv[2])
        if E_flag != "P":
            print convert_c("输入的执行标志位有误")
            sys.exit()
            
        if not (month.isdigit() or month == 'ALL'):
            print convert_c("输入的处理月份有误 正确处理月份应类似于201803")
            sys.exit()
        str_processer.write_res_xls( str_processer.addr_main_process(month) )
    
    elif len(sys.argv) == 2:
        E_flag = sys.argv[1]
        #情况2 输入参数为一个 执行标志位为P 默认生成上个月的处理excel
        if E_flag == "P":
            str_processer.write_res_xls( str_processer.addr_main_process() )
        #情况3 输入参数为一个 执行标志位为U 将处理结果sample_result.xls写入数据库
        elif E_flag == "U":
            str_processer.upload_info_toDB()
        else:
            print convert_c("输入的参数有误")
            sys.exit()
    else:
        print convert_c("输入的参数有误")
        sys.exit()
        
    #unit_test()
    #print str_processer.get_addr_ID("410304198603162530")
