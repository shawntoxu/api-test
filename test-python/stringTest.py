#coding=utf8
'''

@author: shawn.wang
'''

def getRes():
    return None

if __name__ == '__main__':
    a = "abc"
    b = "abcd"
    if a==b:
        print "ok"
        
    #test replace method
    print a.replace('a','s')
    print a+b
    
    aa=1
    print 'ccc'+str(aa)

    e="a1  b2     c3"
    lists=e.split()
    print lists,len(lists)

    d="{host:'AMZ-SIN-Zabbix-255-21',service:'abc.service.test',content:'abc.is.down '}"
    print d.replace('.','-')

    arg="label 172.30.10.175 usergroup=pmd 2"
    list=arg.split()
    if len(list) != 3:
        print 'is not equals 3 .'
    print list[0:2]

    if getRes() is not None:
        print "ok"

    
