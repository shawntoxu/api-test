# -*- coding: UTF-8 -*-
import  thread
import time

import threading



def print_time(ThreadName,delay):
    count = 0
    while count < 15:
        time.sleep(delay)
        count += 1
        print "%s: %s" %(ThreadName,time.ctime(time.time()))



class CacheThread(threading.Thread):

    def __init__(self,name,delay):
        threading.Thread.__init__(self)
        self.name  = name
        self.delay = delay

    def run(self):
        print_time(self.name,self.delay)



# try:
#
#     thread.start_new_thread(print_time('thread-1',1))
#     '''
#       终端无法显示thread2 启动
#     '''
#     thread.start_new_thread(print_time('thread-2',2))
# except:
#     print 'exception'
thread1 = CacheThread('thread-1',2)
thread2 = CacheThread('thread-2',1)

thread1.start()
thread2.start()

