#coding=utf8

import urllib
import urllib2 
import json

import requests

API_ADDR='172.30.80.23:8080'
NAMESPACE='default'
POD_NAME='paas-agent-g0g6q'
url='http://{}/api/v1/namespaces/{}/pods/{}'.format(API_ADDR,NAMESPACE,POD_NAME)


COMMAND="ls /"
# exec_url="http://{}/api/v1/namespaces/{}/pods/{}/exec?container={}&command={}
exec_url="http://{}/api/v1/namespaces/{}/pods/{}/exec?command={}".format(API_ADDR,NAMESPACE,POD_NAME,COMMAND)


def getPodInfo():
    print  url
    response=requests.get(url)

    jresult=response.json()

    print jresult['kind']

    #get hostip
    print jresult['status']['hostIP']

    #get image
    print jresult['status']['containerStatuses'][0]['image']
    for i in jresult['spec']['containers']:
        print i['name']

def execCmd():
    #exec api 必须要websocket 模式执行
    response=requests.get(exec_url)
    jresult=response.json()
    print jresult

if __name__ == '__main__':
    # getPodInfo()
    # execCmd()