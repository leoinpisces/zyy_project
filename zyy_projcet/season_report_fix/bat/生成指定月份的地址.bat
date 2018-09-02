@echo off
echo 请输入需要生成的月份 形式如 201803
set /p date=我输入的是:
C:\Python27\python.exe E:\project\season_report_fix\src\season_report_fix.py P %date%

pause