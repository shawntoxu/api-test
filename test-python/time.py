#coding:utf-8
'''
@author: shawn.wang
'''

import datetime,time
import os

import  pytz

'''
计算2个时间点的时间间隔
通常用于计算软件从启动到 现在的运行时长

time2  一般为当前时间 
time1 启动时间
'''
def calc_time_delta(time2, time1):
    str = ""
    delta = int(time.mktime(time2) - time.mktime(time1))
    days = delta / (3600 * 24)
    hours = delta / 3600
    mins = delta / 60
    seconds = delta
    if days > 0:
        str = "{}d".format(days)
    elif hours > 0:
        str = "{}h".format(hours)
    elif mins > 0:
        str = "{}m".format(mins)
    elif seconds > 0:
        str = "{}s".format(seconds)

    return str

def calc_time_delta2(time_sec,delay_days=3):
    time_sec = int(time_sec)
    days = time_sec / (3600 * 24)
    if days > delay_days:
        return  True
    else:
        return False



def getFileCreateTime(file):
    # return os.stat('E:\logs\log.log').st_ctime
    return os.stat(file).st_ctime


def getFileCreateTimeToNow(file):
    return now - os.stat(file).st_ctime


def getToday():
    return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d'))

def getComponent(file_path):
    #filepath ='/dianyi/log/ym-sync/prod/172.20.84.13'
    return str(file_path.split('/')[3])

BAK_DIR=''

#return a,b
#a is status code
#b is standout
def execCmd(cmd):
    return commands.getstatusoutput(cmd)

def baklog(log_path):
    for dir_path,subpaths,files in os.walk(log_path,False):
        for file in files:
            file_path=os.path.join(dir_path,file)
            if os.path.isfile(file_path):
                #do gzip
                if os.path.exists(BAK_DIR) is False:
                    os.mkdir(BAK_DIR)
                bak_path=BAK_DIR+'/'+getToday +'/'+getComponent(file_path)
                if os.path.exists(bak_path) is False:
                    #os.mkdir(BAK_DIR+'/'+b)
                    execCmd('mkdir -p '+bak_path)
                execCmd('gzip '+file_path)
                print 'mv '+file_path+'.gz '+ bak_path
                execCmd('mv '+file_path+'.gz '+ bak_path)
                #print file_pathyy

if __name__ == '__main__':

    curr_time = time.gmtime()
    print calc_time_delta(curr_time,time.strptime('2017-09-25T05:21:04Z','%Y-%m-%dT%H:%M:%SZ'))



    #get date  2017-04-12 00:00:00 
    date_begin = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    print 'get date is ' + str(date_begin)
    ts_begin = time.mktime(date_begin.timetuple())
    #get number of date 
    print 'get time long is ' + str(ts_begin)
    
    #convert  timestamp to utc date
    convertDate=datetime.datetime.utcfromtimestamp(int('1492992000')).strftime('%Y-%m-%d %H:%M:%S')
    print convertDate
    #get type

    print type(convertDate)
    
    #print type(())  

    #print now time
    now = int(time.time())

    current_time=datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    print 'system timezone  time now is {}'.format(current_time)


    utc_current_time=datetime.datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')

    print 'utc time now is '+str(utc_current_time)
    #print now - 1496281222


    # another method convert timezone
    tz  = pytz.timezone('Asia/Shanghai')
    print datetime.datetime.fromtimestamp(now,tz).strftime('%Y-%m-%d %H:%M:%S')

    #utc_current_time=datetime.datetime.utcfromtimestamp(os.stat('E:\logs\log.log').st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    utc_current_time=datetime.datetime.fromtimestamp(os.stat('E:\logs\log.log').st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    print 'utc time now is '+str(utc_current_time)

    print '-----------------------------'
    over = time.time()  - os.stat('E:\logs\log.log').st_ctime

    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')


    print calc_time_delta2(over,3)

    # os.path.walk('E:/1.2', backlog, None)
    for dir_path,subpaths,files in os.walk('E:/1.2',False):
        for file in files:
            file_path=os.path.join(dir_path,file)
            if os.path.isfile(file_path):
                print file_path
    print getToday() + '/' + getComponent('/dianyi/log/ym-sync/prod/172.20.84.13')


