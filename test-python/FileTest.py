#coding=utf8

import readline
import os

if __name__ == '__main__':
   if os.path.exists("/javatool/a.txt"):
        print "ok"
   try:     
       f=file("/javatool/a.txt","r+w")
       # read()一次全部读取完
       print f.read()
       print "------------"
       f.write("adfasdfasdf\r")
       print f.read()
   except Exception,e:
       print e
   finally:
        f.close()

#append to file
def write_cache(app_json):
    try:
        f=file("/tmp/app.json","a")
        f.writelines(app_json)
    except Exception,e:
        LOG.info(e.message)
    finally:
        f.close()

def read_cache(app_name):
    try:
        if os.stat("/tmp/app.json").st_size==0:
            return None
        LOG.info("get ccc")
        file=open("/tmp/app.json","r")
        for line in file:
            #LOG.info(line)
            if line.split("@")[0] == app_name:
                return json.dumps(line.split("@")[1])
    except Exception,e:
        LOG.info(e.message)
    finally:z
        file.close()
    return None
