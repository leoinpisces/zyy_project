#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import utilities

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

# #Q360报文body中值为字符串的key名称
G_body_keys = ["USERNAME", "medicalNum", "YLFKFS", "JKKH", "ZYCS", "BAH", "XM", "XB", "CSRQ", "NL", 
               "GJ", "BZYZS_NL", "XSETZ", "XSERYTZ", "CSD", "GG", "MZ", "SFZH", "ZY", "HY", 
               "XZZ", "DH", "YB1", "HKDZ", "YB2", "GZDWJDZ", "DWDH", "YB3", "LXRXM", "GX", 
               "DZ", "DH1", "RYTJ", "ZLLB", "RYSJ", "RYSJ_S", "RYKB", "RYBF", "ZKKB", "CYSJ", 
               "CYSJ_S", "CYKB", "CYBF", "SJZY", "MZD_ZYZD", "JBDM", "MZZD_XYZD", "JBBM", "ZKJB", "QJCS", 
               "QJCGCS", "QZRQ", "ZQSS", "BRLY", "SSLCLJ", "ZYYJ", "ZYZLSB", "ZYZLJS", "BZSH", "ZB", 
               "ZB_JBBM", "ZB_RYBQ", "ZZ_CYBQ", "ZYZD", "ZYZD_JBBM", "XY_RYBQ", "CYBQ", "ZZ1", "ZZ_JBBM1", "ZZ_RYBQ1", 
               "ZZ_CYBQ1", "QTZD1", "ZYZD_JBBM1", "RYBQ1", "CYBQ1", "ZZ2", "ZZ_JBBM2", "ZZ_RYBQ2", "ZZ_CYBQ2", "QTZD2", 
               "ZYZD_JBBM2", "RYBQ2", "CYBQ2", "ZZ3", "ZZ_JBBM3", "ZZ_RYBQ3", "ZZ_CYBQ3", "QTZD3", "ZYZD_JBBM3", "RYBQ3", 
               "CYBQ3", "ZZ4", "ZZ_JBBM4", "ZZ_RYBQ4", "ZZ_CYBQ4", "QTZD4", "ZYZD_JBBM4", "RYBQ4", "CYBQ4", "ZZ5", 
               "ZZ_JBBM5", "ZZ_RYBQ5", "ZZ_CYBQ5", "QTZD5", "ZYZD_JBBM5", "RYBQ5", "CYBQ5", "ZZ6", "ZZ_JBBM6", "ZZ_RYBQ6", 
               "ZZ_CYBQ6", "QTZD6", "ZYZD_JBBM6", "RYBQ6", "CYBQ6", "ZZ7", "ZZ_JBBM7", "ZZ_RYBQ7", "ZZ_CYBQ7", "QTZD7", 
               "ZYZD_JBBM7", "RYBQ7", "CYBQ7", "WBYY", "JBBM1", "BLZD", "JBBM2", "BLH", "YWGM", "GMYW", 
               "SJ", "XX", "RH", "KZR", "ZRYS", "ZZYS", "ZYYS", "ZRHS", "JXYS", "SXYS", 
               "BMY", "BAZL", "ZKYS", "ZKHS", "ZKRQ", "SSJCZBM1", "SSJCZRQ1", "SHJB1", "SSJCZMC1", "SZ1", 
               "YZ1", "EZ1", "QKDJ1", "QKYLB1", "MZFS1", "MZYS1", "SSJCZBM2", "SSJCZRQ2", "SHJB2", "SSJCZMC2", 
               "SZ2", "YZ2", "EZ2", "QKDJ2", "QKYLB2", "MZFS2", "MZYS2", "SSJCZBM3", "SSJCZRQ3", "SHJB3", 
               "SSJCZMC3", "SZ3", "YZ3", "EZ3", "QKDJ3", "QKYLB3", "MZFS3", "MZYS3", "SSJCZBM4", "SSJCZRQ4", 
               "SHJB4", "SSJCZMC4", "SZ4", "YZ4", "EZ4", "QKDJ4", "QKYLB4", "MZFS4", "MZYS4", "SSJCZBM5", 
               "SSJCZRQ5", "SHJB5", "SSJCZMC5", "SZ5", "YZ5", "EZ5", "QKDJ5", "QKYLB5", "MZFS5", "MZYS5", 
               "SSJCZBM6", "SSJCZRQ6", "SHJB6", "SSJCZMC6", "SZ6", "YZ6", "EZ6", "QKDJ6", "QKYLB6", "MZFS6", 
               "MZYS6", "LYFS", "YZZY_JGMC", "WSY_JGMC", "ZZYJH", "MD", "RYQ_T", "RYQ_XS", "RYQ_FZ", "RYH_T", 
               "RYH_XS", "RYH_FZ", "ZFY", "ZFJE", "YLFWF", "BZLZF", "ZYBLZHZF", "ZLCZF", "HLF", "QTFY", 
               "BLZDF", "ZDF", "YXXZDF", "LCZDXMF", "FSSZLXMF", "ZLF", "SSZLF", "MZF", "SSF", "KFF", 
               "ZYL_ZYZD", "ZYZL", "ZYWZ", "ZYGS", "ZCYJF", "ZYTNZL", "ZYGCZL", "ZYTSZL", "ZYQT", "ZYTSTPJG",  
               "BZSS", "XYF", "KJYWF", "ZCYF", "ZYZJF", "ZCYF1", "XF", "BDBLZPF", "QDBLZPF", "NXYZLZPF", 
               "XBYZLZPF", "JCYYCLF", "YYCLF", "SSYCXCLF", "QTF"]

#G_body_keys需查询的数据表
G_body_table = "V_Q360"

#标识G_body_table中一条数据的索引
G_body_index = "medicalNum"

#Q360报文body中值为列表的key以及对应列表元素的名称
G_array_key = {}

#Q360报文body中值为列表的数据 所在的数据表名称 结构为{'key值':'数据表名称'}
G_array_table = {}

#标识G_array_table中一条数据的索引
G_array_index = {}

class Q360(utilities.package):
    def __init__(self):
        utilities.package.__init__(self, G_body_keys, G_body_table, G_body_index, G_array_key, G_array_table, G_array_index)
        self.bussiness_id = "Q360"
    
    
if __name__ == '__main__':
    Q360_obj = Q360()

    #生成包处理对象设置包类型
    package_processor = utilities.package_process("Q360")
    package_processor.set_package(Q360_obj)
    package_processor.sent_package()