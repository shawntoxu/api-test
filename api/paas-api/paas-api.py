from flask import Flask, g
from flask_restful import Resource, Api
import sys
from log import LOG
import os

def usage():
    print "paas-api.py HOST_IP PORT"

if len(sys.argv) != 3:
    usage()
    sys.exit(1)

def save_pid():
    if not os.path.exists('/var/run/paas'):
        os.mkdir('/var/run/paas')

    PID_FILE_PATH = '/var/run/paas/paas-api.pid'
    f = file(PID_FILE_PATH, 'w')
    f.write(str(os.getpid()))
    f.close()

app = Flask(__name__)
api = Api(app)

app.config.from_object('config')

@app.route('/ping')
def ping():
    return 'ok'

from application import ApplicationList, Application, ApplicationPod, ApiApplicationActions, ApiApplicationTemplate
api.add_resource(ApplicationList, '/api/v1/applications')
api.add_resource(Application, '/api/v1/applications/<string:application_name>')
api.add_resource(ApplicationPod, '/api/v1/applications/<string:application_name>/pods/<string:pod_name>')
api.add_resource(ApiApplicationActions, '/api/v1/applications/<string:app_name>/actions')
api.add_resource(ApiApplicationTemplate, '/api/v1/applications/<string:app_name>/template')

from application_controller import ApiApplicationControllerList, ApiApplicationController
api.add_resource(ApiApplicationControllerList, '/api/v1/application_controllers')
api.add_resource(ApiApplicationController, '/api/v1/application_controllers/<string:name>')

from image_checker import ImageChecker
api.add_resource(ImageChecker, '/api/v1/image_checker')

from node import NodeList, ApiNode
api.add_resource(NodeList, '/api/v1/nodes', methods=['PATCH', 'GET' ])
api.add_resource(ApiNode, '/api/v1/nodes/<string:name>', methods=['PATCH', 'GET', 'UPDATE'])

import caas
from caas import CaasManager, CaasInfo, CaasList, PortManager, IsPort, PodInfo

#caas status
api.add_resource(caas.HostRes2, '/api/v1/host_res/')
api.add_resource(caas.PodRes, '/api/v1/pod_res/')

#port control
caas.load_ports(app.config['CAAS_K8S_IP'])
api.add_resource(PortManager, '/api/v1/ports/')
api.add_resource(IsPort, '/api/v1/ports/<int:port>')

api.add_resource(PodInfo, '/api/v1/caas/pods/<string:namespace>')
#api.add_resource(PodInfo, '/api/v1/caas/default/pods/')
#rc op
api.add_resource(CaasInfo, '/api/v1/caas_total/')
api.add_resource(CaasList, '/api/v1/caas/rc/<string:namespace>')
api.add_resource(CaasManager,
'/api/v1/caas/rc/<string:namespace>/<string:rc_name>')

try:
    save_pid()
except Exception as e:
    LOG.error(str(e))
    LOG.error('exit 1')
    sys.exit(1)

LOG.info('Started')
app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=True, threaded=True)

