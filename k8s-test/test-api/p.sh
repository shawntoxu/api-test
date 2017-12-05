echo "" > /var/log/yaas/kube-apiserver.log
#python  test.py
bash send.sh 
cat /var/log/yaas/kube-apiserver.log > temp

