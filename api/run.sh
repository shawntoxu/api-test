docker run -d --name api-test  --restart=always -e  "K8S_IP=172.30.80.23" -e "HEAT_IP=172.30.80.23" -e  "ETCD_IP=172.30.80.23" -e  "ETCD_PORT=4001" -e  "HEAT_USERNAME=admin" -e  "HEAT_PAASWORD=ADMIN_PASS" -p 12306:12306  paas-api:2.0
 
#docker exec -it api-test /bin/bash 

