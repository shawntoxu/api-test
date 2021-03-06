import os 
import commands
import re
'''
  get docker ip dir && del it 
  shawn.wang
'''

#log root dir
ROOT_DIR='/temp/log'

# dir ip  eg. 10.10.1.1 -- /temp/log/xxxx/10.10.1.1
ALL_IP_PATH={}

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
    print ' will del {}'.format(ALL_IP_PATH.get(key))
    r,b=execCmd("rm -rf "+ALL_IP_PATH.get(key))
    if r != 0:
	print 'del dir faild : {} '.format(ALL_IP_PATH.get(key))
