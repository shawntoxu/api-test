import os 
import time
import commands
import re
import logging
import datetime
'''
 del old log that not used currently
 shawn.wang
'''

#log root dir
ROOT_DIR='/tmp/log'
BAK_DIR='/tmp/log/bak'
OPS_DIR='/var/log/yaas'

# dir ip  eg. 10.10.1.1 -- /tmp/log/xxxx/10.10.1.1
ALL_IP_PATH={}

def get_logger(name='del.log'):
    logging.basicConfig(filename=os.path.join(OPS_DIR, name),
                        level=logging.DEBUG,
                        format = '[%(asctime)s] [%(levelname)s] %(message)s')
    log_obj = logging.getLogger(name)

    return log_obj


def isIp(ip):
    if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', ip):  
        return True
    else:
        return False

#return a,b
#a is status code
#b is standout
def execCmd(cmd):
    return commands.getstatusoutput(cmd)


def getFileCreateTimeToNow(file):
    return now - os.stat(file).st_ctime

def filterTime(file_path,delay_days=3):
    time_sec = int(time.time() - os.stat(file_path).st_ctime)
    days = time_sec / (3600 * 24)
    if days > delay_days:
        return  True
    else:
        return False

def getToday():
    return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d'))
def getComponent(file_path):
    #filepath ='/tmp/log/ym-sync/prod/172.20.84.13'
    return str(file_path.split('/')[3])

def baklog(log_path):
    for dir_path,subpaths,files in os.walk(log_path,False):
        for file in files:
            file_path=os.path.join(dir_path,file)
            if os.path.isfile(file_path):
                #do gzip
                if os.path.exists(BAK_DIR) is False:
                    os.mkdir(BAK_DIR)
                #bak_path=BAK_DIR+'/'+getToday +'/'+getComponent(str(file_path))
                bak_path="{}/{}/{}".format(BAK_DIR,getToday(),getComponent(str(file_path)))
                if os.path.exists(bak_path) is False:
                    #os.mkdir(BAK_DIR+'/'+b)
                    execCmd('mkdir -p '+bak_path)
                execCmd('gzip '+file_path)
                print 'mv '+file_path+'.gz '+ bak_path
                execCmd('mv '+file_path+'.gz '+ bak_path)
                #print file_pathyy


log=get_logger()
#get all ip dir
def getIpDir(rootDir): 
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists) 
        if os.path.isdir(path) and isIp(lists):
            ALL_IP_PATH[lists] = path
        if os.path.isdir(path) and not isIp(lists):
            getIpDir(path)

a,b = execCmd("docker  ps | grep  google_containers |  awk '{print $1}' | grep -v CONTA")

#convert to list
list=b.split()
ip_list=[]
for id in list:
    command="docker inspect --format '{{ .NetworkSettings.IPAddress }}' "+id
    a,b = execCmd(command)
    ip_list.append(b)

getIpDir(ROOT_DIR)

# get ip set that not running docker ip
del_key=set(ALL_IP_PATH.keys()) - set(ip_list)

for key in del_key:
    log.info(' will bak {} '.format(ALL_IP_PATH.get(key)))
    baklog(ALL_IP_PATH.get(key))
    log.info(' will del {}'.format(ALL_IP_PATH.get(key)))
    r,b=execCmd("rm -rf "+ALL_IP_PATH.get(key))
    if r != 0:
        log.debug('del dir faild : {} '.format(ALL_IP_PATH.get(key)))
