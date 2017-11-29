#!/usr/bin/env python
#coding=utf-8
from datetime import datetime
from flask import Flask,request,redirect,abort,Response,render_template
import getopt
import json
import math
import os
import sys
import time
import datetime
import requests

app = Flask(__name__)

oneMB = 1024*1024

CPU_USAGE_TIME_SECOND = 1
TEM_PATH = "tem.json"

MODE = 'NEW'
#SERVER='10.7.0.1'
SERVER='172.30.10.185'
#SERVER='10.2.33.10'
SERVER_URL='http://%s:8080'
CONTAINER_SERVER_URL='http://%s:4194'
out_rc_url='/api/v1/namespaces/default/replicationcontrollers'
out_pod_url='/api/v1/namespaces/default/pods'
rc_name_url='/api/v1/namespaces/default/replicationcontrollers/<rc_name>'
port_url='/api/v1/ports/'
is_port_url='/api/v1/ports/<int:port>'
pod_res_url='/api/v1/pod_res/'
host_res_url='/api/v1/host_res/'
node_res_url='/api/v1/nodes/'
template_url='/api/v1/template/'
machine_res_url='/api/v1.0/machine/'
container_res_url='/api/v1.0/containers'
#container_url='/api/v1.0/containers/docker/'
#container_url='/api/v2.0/containers/docker/'
#container_url='/api/v2.0/summary/%s?type=docker'
container_url='/api/v1.2/docker/%s'

def WebFormatTool(strj, ret, msg):
    if MODE != 'NEW':
        return  json.dumps(strj, indent=4)

    out = dict()
    out['data'] = strj
    if ret:
        out['flag'] = 'success'
    else:
        out ['flag'] = 'fail'
    out['msg'] = msg
    return  json.dumps(out, indent=4)

#2015-10-27T16:45:28.251893595+08:00
#2015-10-27T16:45:28.251893
def py_timestr(strj):
    #strj = strj[:(len(strj) - 9)]
    strj = strj[:24]
    return strj

def cpu_float(value):
	if value > 100.0:
		return 100.0
	elif value < 0.0001:
		return 0.0
	else:
		return round(value,4)

def get_interval(cur, prev):
    #print "cur : %s, prev:%s" % (cur, prev)
    cur_date =  datetime.datetime.strptime(py_timestr(cur), '%Y-%m-%dT%H:%M:%S.%f')
    prev_date =  datetime.datetime.strptime(py_timestr(prev), '%Y-%m-%dT%H:%M:%S.%f')
    time_delta = cur_date - prev_date
    ret = (time_delta.seconds * 1000 + time_delta.microseconds) * 1000000
    #print 'time_delta %s, ret:%d' % (time_delta, ret)
    if ret == 0:
        return CPU_USAGE_TIME_SECOND * 1000000000
    return ret

def parse_cpu(core_nums, container_data):
    if (container_data['spec']['has_cpu'] and len(container_data['stats']) > CPU_USAGE_TIME_SECOND):
        data = container_data['stats']
        cur = data[len(data) - 1]
        prev = data[len(data) - CPU_USAGE_TIME_SECOND - 1]
        timeNs = get_interval(cur['timestamp'], prev['timestamp'])
        #print 'raw cur:%s' % cur['cpu']['usage']['total']
        #print 'raw prev:%s' % prev['cpu']['usage']['total']
        raw_usage = cur['cpu']['usage']['total']    \
                    - prev['cpu']['usage']['total']
        #print 'raw_usage:%s, timeNs:%d, core_num:%d' % (raw_usage, timeNs, core_nums)
        #usage = float(raw_usage)/timeNs/core_nums * 100
        usage = float(raw_usage) * 100 /timeNs/core_nums
        #print "usage: ", usage
        return cpu_float(usage)
    return None

def parse_mem(container_data):
    if (container_data['spec']['has_memory']):
        data = container_data['stats']
        item = data[len(data) - 1]
        mem_usage = item['memory']['usage']/oneMB
        #mem_total = machine_data['memory_capacity']/oneMB
        #print "mem : ", mem_usage, mem_total
        #return (mem_usage, mem_total)
        return mem_usage

    return None

# is lock needed?
class Ports:
    def __init__(self,low,high):
        self.begin = int(low + 1)
        self.end = int(high - 1)
        self.used = [0] * (self.end - self.begin + 1)
        self.pos = 0
        self.defined = dict()

    def is_used(self,port):
        print port,self.begin,self.end
        if port > self.end or port < self.begin:
           return self.defined.has_key(port)
        pos = port - self.begin
        print self.used[pos]
        if (self.used[pos] == 0):
            return False
        else:
            return True

    def get(self):
        i = 0
        v = self.pos
        while True:
            if self.used[v] == 0:
                port = v + self.begin
                #self.used[v] = 1
                self.pos = (v + 1) % (self.end - self.begin + 1)
                break
            v = (v + 1) % (self.end - self.begin + 1)
            i = i + 1
            assert(i <= self.end - self.begin)

        return port

    def delete(self,port):
        if port < self.begin or port > self.end:
            self.defined.pop(port)
        else:
            self.used[port - self.begin] = 0

    def set_used(self,port):
        if port < self.begin or port > self.end:
            self.defined[port] = 1
        else:
            self.used[port - self.begin] = 1

    def show(self):
        for i in range(self.end - self.begin + 1):
            print "%d:%d" % (i,self.used[i])

class RContainer:
    def __init__(self,pod_str):
        self.name = ''
        self.status = ''
        self.uuid = ''
        self.cpu = int()
        self.mem = int()
        self.raw = pod_str
        self.ready = False
        self.hostip = ''
    def set_ready(self):
        if self.raw['status']['phase'] != 'Running':
            self.ready = False
            return None
        for stat in self.raw['status']['conditions']:
            if stat['type'] == 'Ready' and stat['status'] == 'True':
                self.ready = True
                #print 'set ready !'
                return None
        self.ready = False
        return None
    def is_ready(self):
        return self.ready
    def parse_data(self):
        self.name = self.raw['metadata']['name']
        self.status = self.raw['status']['phase']
        if self.raw['status'].has_key('hostIP'):
            self.hostip = self.raw['status']['hostIP']
        self.set_ready()
        #print json.dumps(self.raw,indent=4)
        if self.ready:
        #if True:
            #print 'uuid:%s' % self.raw['status']['containerStatuses'][0]['containerID']
            self.uuid = self.raw['status']['containerStatuses'][0]['containerID']
            self.uuid = self.uuid[9:]
            print self.uuid
    def req_resource(self):
        url = (CONTAINER_SERVER_URL + container_url) % (self.hostip, self.uuid)
        #print 'url %s' % url
        r = requests.get(url)
        if r.status_code != 200:
            #print r
            abort(r.status_code)
        strj = r.json()
        #print json.dumps(strj,indent=4)
        #print len(strj['stats'])
        #for __,data in strj.items():
        #    self.cpu = data['latest_usage']['cpu']
        #    self.mem = data['latest_usage']['memory']
        #container_data = strj['/docker/%s'%self.uuid]
        machine_data = get_machine_data(self.hostip)
	num_cores = machine_data['num_cores']
	for __,container_data in strj.items():
        	#num_cores = container_data['spec']['cpu']['limit']
        	self.cpu = parse_cpu(num_cores, container_data)
        	self.mem = parse_mem(container_data)
    def get_res(self):
        res = dict()
        res['status'] = self.status
        res['hostip'] = self.hostip
        res['cpu'] = self.cpu
        res['mem'] = self.mem
        #res['uuid'] = self.uuid
        return res


all_ports = Ports(9000,10000)

def resent_req(url,method):
    if method == 'GET':
        para = request.args
        r = requests.get(url,params=para)
        #print "GET input para%s" % para
    elif method == 'POST':
        para = request.data
        #print "post input para%s" % para
        r = requests.post(url,data=para)
    elif method == 'DELETE':
        r = requests.delete(url)

    strj = r.json()
    #print json.dumps(strj,indent=4)
    if r.status_code == 200 or r.status_code == 201 \
        or r.status_code == 204 or r.status_code == 202:
        #return json.dumps(strj,indent=4)
        return WebFormatTool(strj, True, '')
    else:
        print json.dumps(strj,indent=4)

    return WebFormatTool(strj, False, '')
    #abort(r.status_code)

def delete_rc(url,rc):
    #print "delete rc:%s"%url
    #get rc info
    r = requests.get(url)
    strj = r.json()
    #print json.dumps(strj,indent=4)
    if r.status_code != 200:
        abort(r.status_code)

    #reset rc replicas to 0
    strj['spec']['replicas']=0

    r = requests.put(url,data=json.dumps(strj))

    strj = r.json()
    #print "put res", json.dumps(strj,indent=4)
    if r.status_code != 200:
        abort(r.status_code)

    #get all pod of rc
    pod_url = (SERVER_URL + out_pod_url) % SERVER
    para = {'labelSelector':'name=%s'%rc}
    r = requests.get(pod_url,params=para)
    strj = r.json()
    #print "pod list:%s rc:%s" % (json.dumps(strj,indent=4) , rc)
    for pod in strj['items']:
        for container in pod['spec']['containers']:
            if container.has_key('ports'):
                for port_info in container['ports']:
                    port = port_info['hostPort']
                    #print "reused port",port
                    all_ports.delete(int(port))
        pname = pod['metadata']['name']
        #delete all pod
        purl = (SERVER_URL + out_pod_url + "/%s") % (SERVER,pname)
        requests.delete(purl)

    #delete rc
    return resent_req(url,'DELETE')

def load_ports():
    pod_url = (SERVER_URL + out_pod_url) % SERVER
    r = requests.get(pod_url)
    strj = r.json()
    for pod in strj['items']:
        for container in pod['spec']['containers']:
            if container.has_key('ports'):
                for port_info in container['ports']:
                    port = port_info['hostPort']
                    print "used port:",port
                    all_ports.set_used(int(port))
    print all_ports.defined

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route(port_url)
def get_port():
    port = all_ports.get()
    return WebFormatTool(str(port), True, '')

@app.route(is_port_url)
def is_port(port):
    if all_ports.is_used(port):
        return "True"
    else:
        return "False"

@app.route(out_rc_url, methods=['GET', 'POST', 'DELETE'])
def list_rc():
    url = (SERVER_URL + out_rc_url) % SERVER
    if request.method == 'DELETE':
        return delete_rc
    elif request.method == 'POST':
        data = request.data
        strj = json.loads(data)
        #print json.dumps(strj,indent=4)
        for container in strj['spec']['template']['spec']['containers']:
            if container.has_key('ports'):
                for port_info in container['ports']:
                    port = port_info['hostPort']
                    port_info['hostPort'] = int(port_info['hostPort'])
                    port_info['containerPort'] = int(port_info['containerPort'])
                    #print "used port:",port
                    all_ports.set_used(int(port))
            if container.has_key('volumeMounts'):
                for volume in container['volumeMounts']:
                    volume['readOnly'] = False
        strj['spec']['replicas'] = int(strj['spec']['replicas'])
        request.data = json.dumps(strj)

    return resent_req(url, request.method)

@app.route(rc_name_url, methods=['GET', 'POST', 'DELETE'])
def op_rc(rc_name):
    url = (SERVER_URL + out_rc_url + "/%s") % (SERVER,rc_name)
    if request.method == 'DELETE':
        return delete_rc(url, rc_name)
    return resent_req(url, request.method)

@app.route(out_pod_url)
def get_pod():
    url = (SERVER_URL + out_pod_url) % SERVER
    return resent_req(url, request.method)

@app.route(template_url)
def get_template():
    f = open(TEM_PATH)
    res = json.load(f)
    return json.dumps(res)

def get_machine_data(host):
    url = (CONTAINER_SERVER_URL + machine_res_url) % host
    #print 'machine url:%s' % url
    r = requests.get(url)
    if r.status_code != 200:
        print r
        #print json.dumps(strj,indent=4)
        return None
    strj = r.json()
    return strj

def get_container_data(host):
    url = (CONTAINER_SERVER_URL + container_res_url) % host
    #print 'host url:%s' % url
    r = requests.get(url)
    if r.status_code != 200:
        print r
        #print json.dumps(strj,indent=4)
        return None
    strj = r.json()
    return strj

@app.route(host_res_url)
def get_host_res():
    url = (SERVER_URL + node_res_url) % SERVER
    r = requests.get(url)
    if r.status_code != 200:
        print json.dumps(strj,indent=4)
        abort(r.status_code)

    strj = r.json()
    res = list()
    for node in strj['items']:
        host = dict()
        ip = node['metadata']['name']
        #print 'host ip:%s'% ip
        machine_data = get_machine_data(ip)
        container_data = get_container_data(ip)
        if node['status']['conditions'][0]['status'] == 'True':
            host['status'] = 'Running'
        else:
            host['status'] = 'Offline'

        if machine_data != None and container_data != None:
            cpu = parse_cpu(machine_data['num_cores'], container_data)
            mem_usage = parse_mem(container_data)
            mem_total = machine_data['memory_capacity']/oneMB
            #print "mem : ", mem_usage, mem_total
            host['cpu'] = cpu
            host['mem'] = dict()
            host['mem']['usage'] = mem_usage
            host['mem']['total'] = mem_total
            host['ip'] = ip
        res.append(host)

    return WebFormatTool(res, True, '')

@app.route(pod_res_url)
def get_pod_res():
    url = (SERVER_URL + out_pod_url) % SERVER
    r = requests.get(url)
    strj = r.json()
    #print json.dumps(strj,indent=4)
    if r.status_code != 200 and r.status_code != 201 \
        and r.status_code != 204 and r.status_code != 202:
        print json.dumps(strj,indent=4)
        abort(r.status_code)

    res = dict()
    for pod in strj['items']:
        container = RContainer(pod)
        container.parse_data()
        if container.is_ready():
            container.req_resource()
        res[container.name] = container.get_res()
    #out = json.dumps(res, indent=4)
    #print json.dumps(res, indent=4)
    return  WebFormatTool(res, True, '')

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "usage %s <server> [mode]" % sys.argv[0]
        exit(0)
    SERVER=sys.argv[1]
    if len(sys.argv) == 3:
        MODE = sys.argv[2]
        print "MODE:%s" % MODE
    load_ports()
    app.run(host='0.0.0.0',port=6900,debug=True)

