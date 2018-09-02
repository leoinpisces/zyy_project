#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import pyttsx

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')


def speak_out(voice_str):
    engine = pyttsx.init('sapi5', True)
    rate = engine.getProperty('rate')
    rate = rate - 80
    engine.setProperty('rate', rate)
    engine.say(voice_str)
    engine.runAndWait()
    
if __name__ == '__main__':
    speak_out("请您到10号窗口取药")