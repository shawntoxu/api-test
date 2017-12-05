#curl -X PUT -H "Content-Type: application/json" -d '{"key1":"value"}' "http://172.30.80.38:8081/api/v1/namespaces/default/replicationcontrollers/ecnetwork-shop"
#curl -X PUT -H "Content-Type: application/json" -d 'file=@shop-rc.json' "http://172.30.80.23:8080/api/v1/namespaces/default/replicationcontrollers/ecnetwork-shop"
curl -X PUT -H "Content-Type: application/json;charset=utf-8" -d '/home/k8s-test/test-api/shop-rc.json' "http://172.30.80.23:8080/api/v1/namespaces/default/replicationcontrollers/ecnetwork-shop"
#curl -X PUT -H "application/merge-patch+json" -d '/home/k8s-test/test-api/shop-rc.json' "http://172.30.80.23:8080/api/v1/namespaces/default/replicationcontrollers/ecnetwork-shop"
#curl -X PATCH -H "application/strategic-merge-patch+json" -d '{"spec":{"replicas":2}}'  "http://172.30.80.23:8080/api/v1/namespaces/default/replicationcontrollers/ecnetwork-shop"

