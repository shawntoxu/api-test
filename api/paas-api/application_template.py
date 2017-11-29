from flask import request
import flask
import requests
from flask_restful import Resource
from heatclient.exc import *
from heat import heat_client
from common import *

class ApiApplicationTemplate(Resource):
    def get(self, app_name):
        try:
            template = heat_client.get_stack_template(app_name)

            data = {
                'kind': 'ApplicationTemplate',
                'name': app_name,
                'template': template
            }

            response = flask.make_response(json.dumps(data))
            return response
        except HTTPNotFound as e:
            return make_status_response(404, 'The application <{}> is not running'.format(app_name))
        except Exception as e:
            return make_status_response(500, 'Internal error')

