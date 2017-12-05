import requests 
size = 1
master_ip = '172.30.80.23'
rc_name = 'ecnetwork-shop'

headers = {'Content-Type': 'application/strategic-merge-patch+json'}
payload = '{"spec":{"replicas":%s}}' % size

r = requests.patch("http://{ip}:8080/api/v1/namespaces/default/replicationcontrollers/{n}".format(ip=master_ip, n=rc_name), headers=headers, data=payload)
