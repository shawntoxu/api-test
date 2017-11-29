#!/usr/bin/python 
#coding=utf8
#基本的数据类型

try:
    import os
    import sys
    import time
    import datetime
except ImportError,e:
    import sys
    print "Import err",e
    sys.exit(1)
    
def get_some():
    ''' #这里是函数的默认解析函数__doc__
    echo "me too"
    '''
    print 'just a test fun!'
    
#调用系统命令
def run_service(name):
    os.system("service " + name + " stop")

def if_test(a):
    if a is not None:
        print 'a is not None'
    if a == 'b':
        print 'a is b '
    
    if a == 'c':
        print 'is c '
    elif a == 'd':
        print 'is d'

def map_test():
    am={"a":"b","c":"d"}
    
    for k,v in am.items():
        print k+" : " + v ;
    
    a = "asdf"
    b = "asdf"
    
    if a!=b :
        print "a!=b"
    else:
        print "a=b"
    

    
    '''delta = datetime.datetime.now()-lasttime   #使用datetime.datetime.now()得到当前的时间,然后求时间差

    if delta > datetime.timedelta(minutes=8):   #如果时间差大于 8分钟的话,(如果是8小时则是hours=8,如果是8秒则是 seconds=8)

#    datetime.timedelta()这个方法比较特别，在python.org对这个class的解释是：
        class datetime.timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])'''
    #取得当前时间
    currenttime = datetime.datetime.now()
    
    print currenttime
    
    currdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
    print currdatetime
    
    #将字符串转为datetime格式
    dd = datetime.datetime.strptime("2015-09-15 18:33:42", "%Y-%m-%d %H:%M:%S")
    print dd 
    
    #计算时间差
    timeover = currenttime - dd 
    #时间差值大于20秒
    if timeover > datetime.timedelta(seconds=20):
        print " >  20 "
    #每秒执行一次    
    #while True:
    #    time.sleep(1)
     #   print "----"
        
    
if __name__ == '__main__':
    a = ['adf','cdfe','asdfads','ddd']
    for k in a:
        print k+'--,'
    b='@'.join(a)
    #print b
    
    #get_some()
    '''可以运行函数注释中的 shell 命令
    #os.system(get_some.__doc__)
    #get_some
    '''
    #run_service("mysqld")
    
    #if_test("d")
    
    map_test()
    
    
