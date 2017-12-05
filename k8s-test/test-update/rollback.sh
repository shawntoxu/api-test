#轻量级 rollback 
#./kubectl rolling-update 当前rcname  要更新的 image--image=nginx:1.9.1
#./kubectl rolling-update  my-nginx --image=nginx:1.9.1

kubectl  rolling-update my-nginx my-nginx-2 --rollback
