docker kill api-test && docker rm api-test  
docker ps -a  | grep Exited  | awk '{print $1}' | xargs docker rm 

docker build -t paas-api:2.0 ./ 
