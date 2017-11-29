#coding=utf8
'''
Created on 2015年12月15日
数字格式化
@author: shawn.wang
'''

def version_compare(v1,v2):
    if v1.find("_") != -1: 
        vlist1 = version1.split("_")
    print vlist1
    if v2.find("_") != -1: 
        vlist2 = version1.split("_")
    print vlist2

def get(server):
    if server != None:
        print "not null"

if __name__ == '__main__':
    #float  
    #num1 = float(0.1)
    version1 = "v1.4.4_013R"
    version2 = "v1.4.0_006"
    version_compare(version1, version2)
    
    get()
    
    