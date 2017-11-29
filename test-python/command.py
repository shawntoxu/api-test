#coding=utf8
import os 
import cmd

#cmd 模块可以接收命令，以do_* 函数接收命令 * 就是命令
class mytest(cmd.Cmd):
    #输入tab  abc d  打印出去掉两边空格+| 的字符串
    def do_tab(self,arg):
        print arg.strip() + "|"
    def do_exit(self,arg):
        return "bye"
    def do_ls(self,arg):
#        print "%s: "%type(arg), arg
        os.system(arg)  
    def do_dir(self,arg):
        return os.system(arg)

if __name__ == '__main__':
    
    bb = [1] 
    if bb is not None:
        if len(bb) >= 1:
            print "数组不为空"
        
    aa = mytest()
    #开始接收命令
    aa.cmdloop()