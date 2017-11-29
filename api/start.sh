#!/bin/bash 
echo "K8S_IP = '${K8S_IP}'" >> /opt/paas-api/config.py
echo "HEAT_IP = '${HEAT_IP}'" >> /opt/paas-api/config.py
echo "ETCD_IP = '${ETCD_IP}'" >> /opt/paas-api/config.py
echo "ETCD_PORT = ${ETCD_PORT}" >> /opt/paas-api/config.py
echo "HEAT_USERNAME = '${HEAT_USERNAME}'" >> /opt/paas-api/config.py
echo "HEAT_PASSWORD = '${HEAT_PAASWORD}'" >> /opt/paas-api/config.py
echo "HEAT_AUTH_URL = 'http://${HEAT_IP}:35357/v2.0'" >> /opt/paas-api/config.py
echo "CAAS_K8S_IP = '${K8S_IP}'" >> /opt/paas-api/config.py

#run api 
cd /opt/paas-api; python  paas-api.py 0.0.0.0 12306
/usr/sbin/sshd -D

