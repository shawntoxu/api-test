#coding=utf8

''' 变参接收'''

#接收list
def test(*arg):
    print "args is ",arg
    print "arg[1] is ",arg[1]
#接收k-v对    
def test2(**arg2):
    print "arg2 is ",arg2
#先接收 list ，在接收k-v
def test3(*arg3,**arg4):
    print "arg3 is ",arg3
    print "arg4 is ",arg4

#test(1,2,3)
#test2(a=1,b=2,c=3,d=5)
test3(1,5,67,a=1,b='a')