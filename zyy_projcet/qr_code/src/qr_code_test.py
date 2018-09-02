#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import qrcode

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')


def gen_qrcode():
    qr = qrcode.QRCode(version = 4, error_correction = qrcode.constants.ERROR_CORRECT_M, box_size = 10, border = 4 )
    
    qr.add_data("测试测试".encode('utf-8', 'ignore'))
    qr.make(fit = True)
    img = qr.make_image()
    img.save("test.png")
    
if __name__ == '__main__':
    gen_qrcode()