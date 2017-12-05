#!/bin/bash 

if [ $# != 3 ]; then
      echo " ./j.sh controller  ecnetwork-controller  CONTROLLER_SERVICE"
      echo " ./j.sh core-service  ecnetwork-core-service  CORE_SERVICE"
      echo "./j.sh mq-service  ecnetwork-mq-service  MQ_SERVICE"
      echo " ./j.sh scheduler  ecnetwork-scheduler  SCHEDULER_SERVICE"
      echo " ./j.sh shop  ecnetwork-shop  SHOP_SERVICE"
      echo " ./j.sh web  ecnetwork-web  WEB_SERVICE" && exit
fi

app=$1
cp db-service-rc.json  $app-rc.json
cp db-service-svc.json  $app-svc.json

sed -i s/ecnetwork-db-service/$2/g $app-rc.json  
sed -i s/ecnetwork-db-service/$2/g $app-svc.json  
sed -i s/DB_SERVICE/$3/g $app-rc.json
sed -i s/DB_SERVICE/$3/g $app-svc.json 

echo "#-----------$1----------------------------" >>temp 
echo "$"RC_VERSION_$3=test                        >>temp
echo "$"REPLICAS_$3=1                             >>temp
echo "$"$3_PUBLICIPS=172.30.80.216  >>temp
echo "$"$3_PORT='$USER80'  >>temp
echo "$"$3_CONTAINER_PORT=8080  >>temp
echo "$"CONTAINER_MEMORY_$3=1Gi  >>temp
echo "$"CONTAINER_MEMORY_REQ_$3=512Mi  >>temp
echo "$"UPD_PAUSE_$3=5  >>temp
echo "$"UPD_PERCENTAGE_$3=50  >>temp
echo " " >>temp


