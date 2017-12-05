kubectl delete  svc redis-svc 
kubectl delete rc redis-cache
kubectl delete rc web-server


kubectl create -f redis-cache.yaml 
kubectl create -f redis-service.yaml

kubectl create -f web-server.yaml
yaas pods
