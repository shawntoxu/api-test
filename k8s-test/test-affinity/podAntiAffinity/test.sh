kubectl delete  svc nginx-svc 
kubectl delete rc my-nginx
sleep 5 

 kubectl create -f nginx-service.yaml
 kubectl create -f  nginx-test.yaml
yaas pods  
