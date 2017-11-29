#coding=utf8
if __name__ == '__main__':
#字符串的partition函数 将字符串按照分割符分割为3元的tuple
#如果找不到指定的分隔符，则返回仍然是一个3元的tuple，第一个为整个字符串，第二和第三个为空串
    s = "ab,cd,e";
    a = s.partition(",")
    print a
    
