import sys
import time
import requests
import kubernetes
import eventlet
from eventlet import greenthread
import config
import copy
import etcd
import json
import os
from log import LOG
import pykube
import logging
from alert import *

etcd_client = etcd.Client(host=config.ETCD_SERVER, port=config.ETCD_PORT)
pykube_client = pykube.Client(kube_api_url=config.K8S_API_SERVER,
                              etcd_host=config.ETCD_SERVER,
                              etcd_port=config.ETCD_PORT)
alert_manager_pod = AlertManagerPod()

def get_kube_client(request_headers = None):
    kube_client = kubernetes.Api(base_url='{}/api/v1'.format(config.K8S_API_SERVER),
                                 request_headers=request_headers)
    return kube_client

kube_client = get_kube_client()

class NodeManager:
    closed_nodes = []

    @staticmethod
    def close_node(node_name):
        if NodeManager._set_node_schedulable(node_name, False):
            NodeManager.closed_nodes.append(
                { 'name': node_name, 'closed_time': time.time() }
            )

    @staticmethod
    def open_node(node_name):
        if NodeManager._set_node_schedulable(node_name, True):
            for i in len(NodeManager.closed_nodes):
                if NodeManager.closed_nodes[i]['name'] == node_name:
                    NodeManager.closed_nodes.pop(i)
                    break

    @staticmethod
    def open_timeout_nodes():
        new_closed_nodes = []
        now = time.time()
        for node in NodeManager.closed_nodes:
            if now - node['closed_time'] < 120:
                new_closed_nodes.append(node)
            elif not NodeManager._set_node_schedulable(node['name'], True):
                new_closed_nodes.append(node)
        NodeManager.closed_nodes = new_closed_nodes

    @staticmethod
    def _set_node_schedulable(node_name, schedulable):
        kube_client = get_kube_client(request_headers = {"Content-Type": "application/merge-patch+json"})
        for i in range(3):
            try:
                kube_client.SetNodeSchedulable(node_name, schedulable)
                return True
            except Exception, e:
                print e
                time.sleep(1)
        return False

class MemoryController:
    def __init__(self, warn_percent, fatal_percent):
        self.warn_percent = warn_percent
        self.fatal_percent = fatal_percent

    def to_dict(self):
        return {
            'warn_percent': self.warn_percent,
            'fatal_percent': self.fatal_percent
        }

class ApplicationController:

    def __init__(self, template):
        if 'kind' not in template:
            raise Exception('Template error: kind')
        self.name = template.get('name', None)
        if self.name is None:
            raise Exception('Template error: name')
        self.mail_list = template.get('mail_list', [])
        self.phone_list = template.get('phone_list', [])
        self.enabled = template.get('enabled', True)
        self.memory_controller = None
        if 'memory_controller' in template:
            fatal_percent = template['memory_controller'].get('fatal_percent', 0)
            if type(fatal_percent) is not int:
                raise Exception('Template error: memory_controller')
            warn_percent = template['memory_controller'].get('warn_percent', 0)
            if type(warn_percent) is not int:
                raise Exception('Template error: memory_controller')
            self.memory_controller = MemoryController(warn_percent, fatal_percent)

    def to_dict(self):
        data = {
            'kind': 'ApplicationController',
            'name': self.name,
            'mail_list': self.mail_list,
            'phone_list': self.phone_list,
        }
        if self.memory_controller is not None:
            data['memory_controller'] = self.memory_controller.to_dict()

        return data

def get_app_json(app_name):
    response = requests.get('{}/api/v1/applications/{}'.format(config.PAAS_API_SERVER, app_name))
    app_json = response.json()
    if app_json['kind'] == 'Application':
        return app_json
    else:
        return None

def get_all_apps(is_summary=False):
    response = requests.get('{}/api/v1/applications?summary={}'.format(config.PAAS_API_SERVER, 'y' if is_summary else 'n'))
    apps = response.json()
    return apps

def get_app_controllers():
    response = requests.get('{}/api/v1/application_controllers'.format(config.PAAS_API_SERVER))
    data = response.json()
    controllers = []
    for controller_json in data['items']:
        controllers.append(ApplicationController(controller_json))

    return controllers

def check_app_controller(app_json, app_controller):
    for component in app_json['components']:
        if not check_component(app_json['name'], component, app_controller):
            return

def check_app_controllers():
    controllers = get_app_controllers()
    for controller in controllers:
        if not controller.enabled:
            continue
        LOG.info('check app controller <{}>'.format(controller.name))
        app_json = get_app_json(controller.name)
        if app_json:
            check_app_controller(app_json, controller)

def check_apps():
    apps = get_all_apps(is_summary=True)
    for app in apps['items']:
        check_app(app)

def check_app(app):
    kube_client = get_kube_client()
    app_status = app['stack_info']['stack_status']
    if app_status in ['CREATE_IN_PROGRESS', 'UPDATE_IN_PROGRESS', 'ROLLBACK_IN_PROGRESS']:
        pod_list = pykube_client.get_pods(app['name'])
        for pod in pod_list:
            if (not pod.is_ready() and
                    pod.restart_count >= 1 and
                    pod.container_state is not None and
                    pod.container_state.name == 'waiting' and
                    pod.container_state.reason == 'CrashLoopBackOff' and
                    pod.last_container_state is not None and
                    pod.last_container_state.name == 'terminated' and
                    (pod.last_container_state.reason == 'Error' or pod.last_container_state.reason == 'ContainerCannotRun')):
                # reschedule the pod to another node
                NodeManager.close_node(pod.host_IP)
                kube_client.DeletePods(pod.name, pod.namespace)
                LOG.warning('pod <{}> on node <{}> is rescheduled'.format(pod.name, pod.host_IP))

def monitory_app_status():
    fname = 'monitory_app_status'
    while True:
        LOG.info('{}: start'.format(fname))
        try:
            check_app_controllers()
            check_apps()
        except Exception, e:
            LOG.error('{}: {}'.format(fname, e))

        try:
            NodeManager.open_timeout_nodes()
        except Exception as e:
            LOG.error('NodeManager.open_timeout_nodes(): {}'.format(e))

        LOG.info('{}: done'.format(fname))
        greenthread.sleep(30)

def push_pod_status(namespace, pod_name, pod_container):
    ''' pod_name = namespace/pod_name '''
    key = '/paas/applications/{}/pods/{}'.format(namespace, pod_name) 
    pod_container['timestamp'] = int(time.time())
    value = json.dumps(pod_container)
    etcd_client.write(key, value)

def push_node_status(node_name, node_json):
    key = '/paas/nodes/{}'.format(node_name)
    node_json['timestamp'] = int(time.time())
    node_json['name'] = node_name
    value = json.dumps(node_json)
    etcd_client.write(key, value)

def do_etcd_gc():
    fname = 'do_etcd_gc'
    kube_client = get_kube_client()
    while True:
        LOG.info('{}: start'.format(fname))
        key = '/paas/applications'
        value = etcd_client.read(key)

        namespace_list = []
        for sub_item in value._children:
            namespace_list.append(os.path.basename(sub_item['key']))

        for namespace in namespace_list:
            pod_names = {}
            pod_list = kube_client.GetPods(namespace).Items
            for pod in pod_list:
                pod_names['/paas/applications/{}/pods/{}'.format(namespace, pod.Name)] = None

            key = '/paas/applications/{}/pods'.format(namespace)
            try:
                value = etcd_client.read(key)
                for sub_item in value._children:
                    if sub_item['key'] not in pod_names:
                        etcd_client.delete(sub_item['key'])
                        LOG.info('{} is delete from ETCD'.format(sub_item['key']))
            except Exception, e:
                LOG.error('{}: {}'.format(fname, e))

        LOG.info('{}: done'.format(fname))
        greenthread.sleep(60)

def collect_cluster_resource_usage():
    fname = 'collect_cluster_resource_usage'
    kube_client = get_kube_client()
    while True:
        try:
            LOG.info('{}: start'.format(fname))
            pod_list = kube_client.GetPods().Items
            assert pod_list is not None
            node_list = kube_client.GetNodes()
            assert node_list is not None
            for node in node_list:
                if not node.is_ready():
                    continue

                session = requests.Session()
                #
                # get pod container status
                #
                url = 'http://{}:12305/api/v1.0/docker'.format(node.name)
                try:
                    res = session.get(url)
                    if res.status_code != 200:
                        LOG.warning('Can not connect to agent <{}>'.format(node.name))
                        continue
                except Exception, e:
                    LOG.warning('Can not connect to agent <{}>'.format(e.message))
                    continue
                pod_containers = res.json()
                assert pod_containers is not None
                for key, pod_container in pod_containers.items():
                    found = False
                    for pod in pod_list:
                        try:
                            if pod.Status.ContainerStatuses[0]['containerID'][9:] == key:
                                found = True
                                break
                        except:
                            pass

                    if not found:
                        continue

                    push_pod_status(pod_container['namespace'], pod_container['pod_name'], pod_container)

                #
                # get node status
                #
                url = 'http://{}:12305/api/v1.0/machine'.format(node.name)
                try:
                    res = session.get(url)
                    if res.status_code != 200:
                        LOG.warning('Can not connect to agent <{}>'.format(node.name))
                        continue
                except Exception, e:
                    LOG.warning('Can not connect to agent <{}>'.format(e.message))
                    continue
                node_json = res.json()
                push_node_status(node.name, node_json)
            LOG.info("{}: done".format(fname))
        except Exception, e:
            LOG.error('{}: {}'.format(fname, e))

        greenthread.sleep(30)

def check_component(app_name, component_json, app_controller):
    '''
    If current component's status is OK, return True.
    If current component's status is not OK, return False
    '''
    fname = 'check_component'

    pod_need_killed = None
    is_component_ready = True
    for pod in component_json['pods']:
        alert_manager_pod.check_pod(pod, app_controller)

        if not pod['is_ready'] or not pod['is_running']:
            is_component_ready = False
            break
        try:
            if float(pod['mem_usage'] - pod['mem_cache']) / float(pod['max_mem_limit']) * 100 >= app_controller.memory_controller.fatal_percent:
                pod_need_killed = pod
        except Exception, e:
            LOG.error('{}: {}'.format(fname, e))

    if component_json['replicas'] != len(component_json['pods']):
        return False

    if component_json['replicas'] == 1:
        return True

    if is_component_ready and pod_need_killed:
        # kill the pod
        kube_client.DeletePods(pod_need_killed['name'], namespace=app_name)

        memory_percent = round(float(pod_need_killed['mem_usage'] - pod_need_killed['mem_cache']) / float(pod_need_killed['max_mem_limit']) * 100, 1)
        msg = '{}:{}:mem={}%'.format(app_controller.name, pod['name'], memory_percent)
        alert_record = AlertRecord(key = pod['name'],
                                   alert_type = AlertType.MEM,
                                   alert_level = AlertLevel.ERROR,
                                   timestamp = int(time.time()),
                                   msg = msg,
                                   hostname = pod['host_IP'],
                                   mail_list = app_controller.mail_list,
                                   phone_list = app_controller.phone_list)
        if Alert.alert(alert_record):
            LOG.info('SMS sent: {}'.format(msg))
        LOG.info('{}: Pod <{}> is deleted because its memory usage {}/{}/{} is over {}%'.format(app_name, pod_need_killed['name'], pod_need_killed['mem_cache'], pod_need_killed['mem_usage'], pod_need_killed['max_mem_limit'], app_controller.memory_controller.fatal_percent))
        return False
    elif is_component_ready:
        return True
    else:
        return False

def main(argv):
    # set requests lib log level to warning
    logger = logging.getLogger('requests')
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    eventlet.spawn(monitory_app_status)
    eventlet.spawn(collect_cluster_resource_usage)
    eventlet.spawn(do_etcd_gc)
    while True:
        eventlet.sleep(3600)

if __name__ == '__main__':
    main(sys.argv[1:])

