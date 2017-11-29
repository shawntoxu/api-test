#coding=utf8
#自动登录指定主机 执行命令
try:   
    import paramiko
    import threading
    import sys
except:
    print "no moudle"
def ssh2(ip,username,password,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(hostname=ip, port=22, username=username, password=password, timeout=15)
        ssh.connect(ip, 22, username, password, timeout=15)

        #ssh.connect(hostname, port, username, password, pkey, key_filename, timeout, allow_agent, look_for_keys)
        
        for m in cmd:
            stdin,stdout,stderr = ssh.exec_command(m)
            #stdin.write("Y")
            out = stdout.readlines()
            for o in out:
                print o
                #print '%s\tOK\n'%(ip)
        ssh.close()
    except Exception,e:
        print e
        print "error",ip

if __name__ == '__main__':
        cmd = ["/etc/init.d/iptables status","ls /"]
        username='root'
        password='qwertyuiop'
        thread = []
        print "begin"
        
        ssh2('192.168.10.102',username,password,cmd)
        
        #for i in rang(1,254):
         #   ip = '192.168.10.'+str(i)
         #   a = threading.Thread(target=ssh2,args=(ip,username,password,cmd))
         #   a.start()