#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import serial.tools.list_ports
import string
import binascii

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

G_baud_rate = 9600
G_escape = b"\x7D\x5E"
G_frame_head = b"\x7E\x00\x00\x00\x00\x31"
G_frame_end = b"\x7E"
#\x32表明线路号为\x32 \x01代表数据长度  \x20代表ascii值\x20(空格符) 线路\32的内容默认是不显示的
G_frame_32 = b"\x32\x01\x20"
G_max_byte = 200

G_hex2byte = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', b'\x09', b'\x0A', b'\x0B', b'\x0C', b'\x0D', b'\x0E', b'\x0F', 
              b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15', b'\x16', b'\x17', b'\x18', b'\x19', b'\x1A', b'\x1B', b'\x1C', b'\x1D', b'\x1E', b'\x1F', 
              b'\x20', b'\x21', b'\x22', b'\x23', b'\x24', b'\x25', b'\x26', b'\x27', b'\x28', b'\x29', b'\x2A', b'\x2B', b'\x2C', b'\x2D', b'\x2E', b'\x2F', 
              b'\x30', b'\x31', b'\x32', b'\x33', b'\x34', b'\x35', b'\x36', b'\x37', b'\x38', b'\x39', b'\x3A', b'\x3B', b'\x3C', b'\x3D', b'\x3E', b'\x3F', 
              b'\x40', b'\x41', b'\x42', b'\x43', b'\x44', b'\x45', b'\x46', b'\x47', b'\x48', b'\x49', b'\x4A', b'\x4B', b'\x4C', b'\x4D', b'\x4E', b'\x4F', 
              b'\x50', b'\x51', b'\x52', b'\x53', b'\x54', b'\x55', b'\x56', b'\x57', b'\x58', b'\x59', b'\x5A', b'\x5B', b'\x5C', b'\x5D', b'\x5E', b'\x5F', 
              b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67', b'\x68', b'\x69', b'\x6A', b'\x6B', b'\x6C', b'\x6D', b'\x6E', b'\x6F', 
              b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67', b'\x68', b'\x69', b'\x6A', b'\x6B', b'\x6C', b'\x6D', b'\x6E', b'\x6F', 
              b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78', b'\x79', b'\x7A', b'\x7B', b'\x7C', b'\x7D', b'\x7E', b'\x7F', 
              b'\x80', b'\x81', b'\x82', b'\x83', b'\x84', b'\x85', b'\x86', b'\x87', b'\x88', b'\x89', b'\x8A', b'\x8B', b'\x8C', b'\x8D', b'\x8E', b'\x8F', 
              b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97', b'\x98', b'\x99', b'\x9A', b'\x9B', b'\x9C', b'\x9D', b'\x9E', b'\x9F', 
              b'\xA0', b'\xA1', b'\xA2', b'\xA3', b'\xA4', b'\xA5', b'\xA6', b'\xA7', b'\xA8', b'\xA9', b'\xAA', b'\xAB', b'\xAC', b'\xAD', b'\xAE', b'\xAF', 
              b'\xB0', b'\xB1', b'\xB2', b'\xB3', b'\xB4', b'\xB5', b'\xB6', b'\xB7', b'\xB8', b'\xB9', b'\xBA', b'\xBB', b'\xBC', b'\xBD', b'\xBE', b'\xBF', 
              b'\xC0', b'\xC1', b'\xC2', b'\xC3', b'\xC4', b'\xC5', b'\xC6', b'\xC7', b'\xC8', b'\xC9', b'\xCA', b'\xCB', b'\xCC', b'\xCD', b'\xCE', b'\xCF', 
              b'\xD0', b'\xD1', b'\xD2', b'\xD3', b'\xD4', b'\xD5', b'\xD6', b'\xD7', b'\xD8', b'\xD9', b'\xDA', b'\xDB', b'\xDC', b'\xDD', b'\xDE', b'\xDF', 
              b'\xE0', b'\xE1', b'\xE2', b'\xE3', b'\xE4', b'\xE5', b'\xE6', b'\xE7', b'\xE8', b'\xE9', b'\xEA', b'\xEB', b'\xEC', b'\xED', b'\xEE', b'\xEF', 
              b'\xF0', b'\xF1', b'\xF2', b'\xF3', b'\xF4', b'\xF5', b'\xF6', b'\xF7', b'\xF8', b'\xF9', b'\xFA', b'\xFB', b'\xFC', b'\xFD', b'\xFE', b'\xFF']

class serial_tools():
    def __init__(self):
        self.port_name_list = []
        self.port_list = []
        self.fd_dict = {}
        
        self.get_ports()
        self.get_ports_names()
        self.init_port()
    
    #获取可用端口列表    
    def get_ports(self):
        self.port_list = list(serial.tools.list_ports.comports())
        
    #填写可用端口名称列表
    def get_ports_names(self):
        for index in range(len(self.port_list)):
            self.port_name_list.append( str(self.port_list[index][0]) )
            
    #创建端口 默认波特率9600 如果端口被占用 是无法创建serial对象的
    def init_port(self):
        for item in self.port_name_list:
            try:
                self.fd_dict[item] = serial.Serial(port = item, baudrate = G_baud_rate, timeout = 1)
            except serial.serialutil.SerialException:
                self.fd_dict[item] = None
                continue
            
    #析构函数 关闭端口
    def __del__(self):
        if self.fd_dict:
            for key in self.fd_dict.keys():
                if self.fd_dict[key]:
                    self.fd_dict[key].close()
                
class gen_infostr():
    #数据中遇到0x7E时要插入转义字符
    def insert_escape(self, raw_str):
        if len(raw_str) == 0:
            return raw_str
        #记录插入转义字符前的原始字符串长度
        length = len(raw_str)
        
        for index in range(length):
            if raw_str[index] == G_frame_end:
                #插入转义字符
                raw_str = raw_str[:index + 1] + G_escape + raw_str[index + 1:]
                #重新设置字节串长度
                length = len(raw_str)
                #调整索引
                index = index + len(G_escape) 
        return raw_str
    
    #字节串按位异或 
    def byte_xor(self, byte1, byte2):
        byte1_list = list(byte1)
        byte2_list = list(byte2)
        
        if len(byte1_list) != len(byte2_list):
            return None
        xor_byte = ""
        #按位异或
        for index in range(len(byte1_list)):
            temp_result = ord(byte1_list[index]) ^ ord(byte2_list[index])
            xor_byte = xor_byte + chr(temp_result)
        
        return xor_byte
    
    #计算校验和
    def gen_check_sum(self, raw_str):
        if len(raw_str) == 0:
            return raw_str
        
        length = len(raw_str)
        check_sum = raw_str[0]
        
        for index in range(1, length):
            check_sum = self.byte_xor(check_sum, raw_str[index])
            
        return check_sum
    
    #生成需发送的字符串 最长支持200字节即100汉字
    def gen_infostr(self, raw_str):
        if len(raw_str) > G_max_byte:
            return None
        
        #首先插入转义字符
        escape_str = self.insert_escape(raw_str)
        info_length = "" 
        
        try:
            info_length = G_hex2byte[len(escape_str)]
        except IndexError:
            return None
            
        info_str = G_frame_head + info_length + escape_str + G_frame_32
        
        return (info_str + self.gen_check_sum(info_str) + G_frame_end)
        
if __name__ == '__main__':
    serial_obj = serial_tools()
    str_gener = gen_infostr()
    
    
    if len(sys.argv) == 1:
        info_str = "重庆市中医院祝您身体健康！！！"
    else:
        info_str = sys.argv[1].strip().decode('cp936').encode('utf-8')
        
    data = str_gener.gen_infostr(info_str.decode('utf-8').encode('cp936'))
    
    for index in range(len(serial_obj.port_name_list)):    
        if serial_obj.fd_dict[serial_obj.port_name_list[index]]:
            serial_obj.fd_dict[serial_obj.port_name_list[index]].write(data)        
    

#帧头  信息方向  设备编号  功能设置  显示模式  线路号31  数据长度    数据体(放射科请张三就诊)                             线路号32  数据长度   数据体(空格) 校验和(前面所有字节的异或)  帧尾
#7E  00      00      00     00     31       10       B7 C5 C9 E4 BF C6 C7 EB D5 C5 C8 FD BE CD D5 EF  32       01      20          2A                      7E
#条屏分为两条线路 \x31和\x32 一个数据帧要包含两条线路帧 但由于硬件限制值显示了31 
    