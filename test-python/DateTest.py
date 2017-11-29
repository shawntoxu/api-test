#coding=utf8

import datetime 
import time

#取得前一天的时间 开始 到结束的时间秒数
def day_get(d,p='from'):
    oneday = datetime.timedelta(days=1)
    day = d - oneday
    if p == 'from':
        date_from = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
        #print "from: %s" % date_from
        return time.mktime(date_from.timetuple())
    if p == 'to':
        date_to = datetime.datetime(day.year, day.month, day.day, 23, 59, 59)
     #   print "to: %s" % date_to
        return time.mktime(date_to.timetuple())
    return 'error'


def  test():
    a="%s_%s " % (int(start),(to))
    print a

if __name__ == '__main__':
    #pass
    #取得一天时间
    oneday = datetime.timedelta(days=1)
    d = datetime.datetime.now()
    print d
    print d-oneday 
#     print d
    start=day_get(d, 'from')
    to=day_get(d, 'to')
    print start,to
    
    test()
    #计算前几天数据
    oneday2 = datetime.timedelta(days=18)
    print d-oneday2