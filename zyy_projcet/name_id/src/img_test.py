#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime
import win32com
from win32com.client import Dispatch, constants
import ImageGrab
import win32clipboard
#import win32con

#WdPasteDataType

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

G_word_obj = win32com.client.DispatchEx('Word.Application')
G_word_obj.Visible = 0
G_word_obj.DisplayAlerts = 0

def read_word(file_path):
    try:
        doc_file = G_word_obj.Documents.Open(file_path)
    except:
        return -1
    return doc_file
    
    print "read"

if __name__ == '__main__':
    
    try:
        doc_file = read_word(r'F:\temp\report.doc'.decode('utf-8').encode('cp936'))
        doc_file.Select()
        doc_file.ActiveWindow.Selection.CopyAsPicture()
        try:
            for para in G_word_obj.ActiveDocument.Paragraphs:
                para.Range.Delete()
        except:
            print "delete failed"
            
        try:
            doc_file.ActiveWindow.Selection.PasteSpecial(False, False, False, False, 4, False, False)
        except:
            print "PasteSpecial failed"
        
        doc_file.Save()
                        
        doc_file.Select()
        doc_file.ActiveWindow.Selection.CopyAsPicture()
        img = ImageGrab.grabclipboard()
        if isinstance(img, ImageGrab.Image.Image):
            print "image"
        else:
            print "not image"
        
        doc_file.Close()
    except:
        print "some error"
        G_word_obj.Quit()
        
    finally:
        G_word_obj.Quit()
        
    #img.save(r'F:\temp\test.jpg'.decode('utf-8').encode('cp936'),'jpg')
        
    print 'OK'