#-*-encoding:utf-8-*-
import os
import sys
'''
@author: shawn.wang
list all filename of dir
'''

if __name__ == '__main__':
    info=raw_input("请输入要列举文件的目录名称：(如D:\\temp)")
    listfile=os.listdir(info)
    print listfile
    for line in listfile:
        #eclipse 中使用这一行
        #print line.decode('gbk').encode('utf-8')
        #cmd 中使用这一行
        print line