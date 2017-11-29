#FROM paas-api 
FROM xa.repo.ndp.com:5000/paas/ubuntu-sshd 

ADD ./paas-api  /opt/paas-api
ADD ./kubernetes /usr/local/lib/python2.7/dist-packages/kubernetes
RUN wget  https://bootstrap.pypa.io/get-pip.py && python get-pip.py \
&& apt-get install python-heatclient -y \
&& pip install flask flask_restful \ 
&& pip install  etcd \
&& pip install python-etcd  && mkdir /var/log/yaas/
ADD ./start.sh  /root/start.sh 

EXPOSE 12306 
CMD ["/bin/sh","-c","/root/start.sh"]


