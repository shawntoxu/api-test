#kubectl run -i --tty load-generator --image=busybox:latest /bin/sh #进入容器后执行一下命令


# 172.10.0.240  is cluster ip address 

while true;do wget -q -O- http://172.10.0.240; done 
