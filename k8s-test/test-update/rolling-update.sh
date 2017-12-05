#kubectl rolling-update my-nginx --image=nginx:1.9.1
#kubectl rolling-update my-nginx --image=nginx:1.7.9  --rollback=true


kubectl rolling-update my-nginx -f ./nginx-1.9.1.yaml
