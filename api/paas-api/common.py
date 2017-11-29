import etcd
import config
import kubernetes
import flask
import json
import uuid
import os
import datetime

etcd_client = etcd.Client(host=config.ETCD_IP, port=config.ETCD_PORT)

base_url = 'http://%s:8080/api/v1' % (config.K8S_IP)
kube_client = kubernetes.Api(base_url=base_url)

def make_status_response(code, message=''):
    response = flask.make_response(json.dumps({'kind': 'Status', 'code': code, 'message': message}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def dump_app_json_into_file(namespace, content):
    DIR = '/tmp/paas'
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    file_name = '{}/{}.{}'.format(DIR, datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f"), namespace)
    file_obj = file(file_name, 'w')
    file_obj.write(content)
    file_obj.close()
    return file_name

