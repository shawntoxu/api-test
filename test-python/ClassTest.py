#coding=utf8

class ClassTests(object):
    #类属性
    address = 'home'
    
    #统计类被创建多少次
    count  = 0 
    
    #
    __test = "test"
    
    def __init__(self,name,age,weight,height,**args):
        self.name = name
        self.age = age
        # 以双下划线开头的属性为私有属性
        self.__weight = weight
        # 但是以双下划线开头并且以双下划线结尾的属性 又可以被访问了
        self.__height__ = height
        
        #每次有实例创建时让统计器+1
        ClassTests.count += 1
        #通过动态参数核 setattr 来动态的添加属性
        for(key,value) in args.items():
            setattr(self, key, value)
    
    #通过函数访问私有属性    
    def  fun(self):
        return self.__test
    
    #通过类访问访问  @classmethod 为类方法标志 cls 为类本身
    @classmethod
    def cls_method(cls):
        return cls.__test



if __name__ == '__main__':
    instance = ClassTests("wx",20,10,50)
    print instance.name + "," +str(instance.age)
    
    #实例不能访问双下划线的属性
    #print instance.__weight
    
    print instance.__height__
    
    #通过动态参数增加实例的属性
    instance = ClassTests("wx",20,10,50,sex='f')
    print instance.sex
    
    # 直接访问类属性
    print ClassTests.address
    #通过实例访问类属性 
    print instance.address  
    
    
    print  r''' python 为动态语言 动态的改变类属性后'''
    
  
    ClassTests.address  = 'home-change'
    #再次访问的时候 类属性已经改变了 
    print ClassTests.address
    #通过实例访问类属性 
    print " 通过实例访问类属性 " + instance.address  
    
    instance = ClassTests("wx2",20,10,50)
    instance = ClassTests("wx3",20,10,50)
    print "类被创建了",ClassTests.count,"次"
    
    #不能直接访问__开头的类属性 可通过方法访问
    #print instance.__test
    print instance.fun()
    #通过类方法访问
    print ClassTests.cls_method()
    
    #使用isinstance 判断实例是否为某个类型
    print isinstance(instance, ClassTests)
    
    #打印instance 的所有属性和方法
    ''' dir(s) 可以打印出制定变量s的所有属性 '''
    print dir(instance)
    
    
    
    