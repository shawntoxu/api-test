#coding=utf8
'''
Created on 2015��11��12��
lsit test 
@author: shawn.wang
'''

def setTest():
    a = set([1,2,3,4,5,6])
    b = set([2,4])
    c = set([8,9])
    #求差集（项在a中，但不在b中） 
    d = a - b 
    print d
    #求并集（项在a中b中）
    e = a | c 
    print e
    
    #交集 &
    
    #对称差集 （项在a或b中，但不会同时出现在二者中）
    f = a ^ b 
    print  f
    
    
    #new a list by  set 
    newlist = list(a)
    print newlist 
    pass 




if __name__ == '__main__':
    setTest()
    #     cc = ['d'];
    #     #is null
    #     if  len(cc):
    #         print cc

    #old_rc=None
    #print 'old_rc==='+old_rc.__str__
    test_ip = '172.30.80.199'
    ACCOUNT=['172.30.80.127','172.30.80.128']
    ACCOUNT.append('aaa')
    print ACCOUNT
    if test_ip not in ACCOUNT:
        print 'ok'

