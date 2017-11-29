#coding=utf8
import xlrd
import smtplib  
from email.mime.text import  MIMEText  
'''
@author: shawn.wang
'''

def sendmail(to):
    _user = "xxxx@qq.com"  
    _pwd  = "bnlfkkhkqgxcbddd"  
    _to   = to 
    
    msg = MIMEText("sbuject")  
    msg["Subject"] = "我 是"  
    msg["From"]    = _user  
    msg["To"]      = _to  
    
    s = smtplib.SMTP("smtp.qq.com",465)
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    s.close()  

if __name__ == '__main__':
    data = xlrd.open_workbook('f:\mail.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    #get all row
#     for i in range(nrows):
#       print table.row_values(i)
#     table.row_values(0)
    #get 1 col 
    col2 = table.col_values(0)
    for j in col2:
        print j
        sendmail(j)