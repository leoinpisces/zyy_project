#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2017-09-21

@author: leoinpisces
'''

import sys
import os
import re
import datetime
from suds.client import Client
import get_webservices as gw
import xml.sax
import xml.dom.minidom
import suds

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#preInpPay(xs:string username, xs:string password, xs:string invokeDate, xs:string hospCode, 
#          xs:string areaCode, xs:string inpNo, xs:string opertator, xs:string redeemDate, 
#          xs:string redeemOrgno, xs:base64Binary inpDatas, )

G_body_dict = {}


G_body_list = ["N706-01", "N706-02", "N706-03", "N706-04", "N706-05", "N706-06", "N706-07", "N706-08", "N706-09", "N706-10", "N706-11", "N706-12", "N706-13",
               "N706-14", "N706-15", "N706-16", "N706-17", "N706-18", "N706-19", "N706-20", "N706-21", "N706-22", "N706-23", "N706-24", "N706-25", "N706-26",
               "N706-27", "N706-28", "N706-29", "N706-30", "N706-31", "N706-32", "N706-33", "N706-34", "N706-35", "N706-36", "N706-37", "N706-38", "N706-39",
               "N706-40", "N706-41", "N706-42", "N706-43", "N706-44", "N706-45", "N706-46", "N706-47", "N706-48", "N706-49", "N706-50", "N706-51", "N706-60",
               "N706-52", "N706-53", "N706-54", "N706-55", "N706-56", "N706-57"]

class success_handler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.hospital_id = ""
        
class fail_handler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data = ""

#总装xml文件
def assemble_xml():
    doc = xml.dom.minidom.Document()
    root = doc.createElement("NDEML")
    root.setAttribute("templateVersion", "1.0")
#     root.setAttribute("xmlns", "urn:hl7-org:v3")
#     root.setAttribute("xmlns:mif", "urn:hl7-org:v3/mif")
#     root.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
#     root.setAttribute("xsi:schemaLocation", "urn:hl7-org:v3 ..\sdschemas\CDA.xsd")
    #装入header
    root.appendChild( create_header(doc) )
    #装入数据体
    root.appendChild( create_body(doc) )
    
    doc.appendChild(root)
    result = bytearray( doc.toxml(encoding = 'UTF-8') )
    
    pretty_result = bytearray( doc.toprettyxml(encoding = 'UTF-8') )
    print pretty_result
    
    return result

#生成xml文件的头部 要求传入monidom的document对象
def create_header(doc):
    node_header = doc.createElement("header")
    #写入导出时间
    node_exportDate = doc.createElement("exportDate")
    node_exportDate.appendChild(doc.createTextNode(gw.G_invoke_time))
    node_header.appendChild(node_exportDate)
    #写入业务数据类型
    node_dataType = doc.createElement("dataType")
    node_dataType.appendChild(doc.createTextNode("N706"))
    node_header.appendChild(node_dataType)
    #写入数据来源
    node_sourceCode = doc.createElement("sourceCode")
    node_sourceCode.setAttribute("ref", gw.G_hospital_id)
    node_sourceCode.appendChild( doc.createTextNode(gw.convert("重庆市中医院") ))
    node_header.appendChild(node_sourceCode)
    #写入数据目标
    node_targetCode = doc.createElement("targetCode")
    node_targetCode.setAttribute("ref", "00")
    node_targetCode.appendChild( doc.createTextNode( gw.convert("国家平台") ) )
    node_header.appendChild(node_targetCode)
    #写入数据来源类型
    node_sourceType = doc.createElement("sourceType")
    node_sourceType.setAttribute("ref", "1")
    node_sourceType.appendChild( doc.createTextNode(gw.convert("医院上传") ) )
    node_header.appendChild(node_sourceType)
    
    return node_header

#构造数据体
def create_body(doc):
    node_body = doc.createElement("body")
    node_data = doc.createElement("data")
    node_706 = doc.createElement("706")
    
    for item in G_body_list:
        if G_body_dict.has_key(item):
            node_item = doc.createElement(item)
            node_item.appendChild( doc.createTextNode( gw.convert( G_body_dict[item] ) ) )
            node_706.appendChild(node_item)
            
    node_data.appendChild(node_706)
    node_body.appendChild(node_data)
    
    return node_body

def send_data(xml_str):
    services = gw.U_get_services(gw.G_url)
    #如果没有获取到有效服务返回0 表示调用失败
    if services is None:
        return 0
    #调用webservice服务
    try:
        result = services.preInpPay(gw.G_username, gw.G_password, gw.G_invoke_time, gw.G_hospital_id, )
    
    except suds.WebFault, ex:
        print ex.fault
        print ex.document
    print result
    return result
    
if __name__ == '__main__':
    result = assemble_xml()