import requests
import etcd
from .pod import Pod

class Client():
    def __init__(self, kube_api_url, etcd_host, etcd_port):
        self.kube_api_url = kube_api_url
        self.etcd_client = etcd.Client(host=etcd_host, port=etcd_port)

    def get_pods(self, namespace):
        pods = []
        url = '{}/api/v1/namespaces/{}/pods'.format(self.kube_api_url, namespace)
        response = requests.get(url)
        for item in response.json()['items']:
            pods.append(Pod(item))

        return pods
