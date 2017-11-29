from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import requests
import flask
from __main__ import app
import json
from copy import deepcopy
import datetime
import time
from keystoneclient.v2_0 import client as keystone_client
from heatclient.client import Client as heat_client
from heatclient.exc import *
import heatclient
import copy
from flask_restful import Resource
import re
import timeit
from log import LOG
from common import etcd_client
import etcd
import os

class MemoryController:
    def __init__(self, warn_percent, fatal_percent):
        self.warn_percent = warn_percent
        self.fatal_percent = fatal_percent

    def to_dict(self):
        return {
            'warn_percent': self.warn_percent,
            'fatal_percent': self.fatal_percent
        }

'''
{
    "kind": "ApplicationController",
    "name": "app1",
    "mail_list": [
        "allen@yeahmobi.com",
        "jeff@yeahmobi.com"
    ],
    "memory_threshold": 95,
    "phone_list": [
        "1819100001",
        "1390002323"
    ],
    "memory_controller": {
        "fatal_percent": 95,
        "warn_percent": 90
    }
}
'''
class ApplicationController:

    def __init__(self, template):
        if 'kind' not in template:
            raise Exception('Template error: kind')
        self.name = template.get('name', None)
        if self.name is None:
            raise Exception('Template error: name')
        self.memory_threshold = template.get('memory_threshold', 999)
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
            'memory_threshold': self.memory_threshold,
            'mail_list': self.mail_list,
            'phone_list': self.phone_list,
            'enabled': self.enabled,
        }
        if self.memory_controller is not None:
            data['memory_controller'] = self.memory_controller.to_dict()

        return data

def _is_template_valid(template):
    if 'kind' not in template \
        or 'name' not in template\
        or 'memory_threshold' not in template:
        return False
    if template['kind'] != 'ApplicationController' \
        or template['name'] == '' \
        or type(template['memory_threshold']) is not int\
        or template['memory_threshold'] < 50:
        return False

    return True

class ApiApplicationControllerList(Resource):
    '''
    {
        "type": "ApplicationControllerList",
        "name": "fb-pmd-01",
        "memory_threshold": 900
    }
    '''
    def post(self):
        template = request.get_json()
        try:
            controller = ApplicationController(template)
        except:
            return flask.make_response(json.dumps({'kind': 'Status', 'code': 400}))

        key = '/paas/application_controllers/{}'.format(template['name'])
        value = json.dumps(controller.to_dict())
        etcd_client.write(key, value)

        return flask.make_response(json.dumps({'kind': 'Status', 'code': 200}))

    def get(self):
        key = '/paas/application_controllers'
        items = []
        try:
            value = etcd_client.read(key)
            for sub_item in value._children:
                key = sub_item['key']
                value = etcd_client.read(key).value
                items.append(json.loads(value))
        except:
            pass

        reply = {
            'kind': 'ApplicationControllerList',
            'items': items
        }
        response = flask.make_response(json.dumps(reply))
        return response

class ApiApplicationController(Resource):

    def get(self, name):
        key = '/paas/application_controllers/{}'.format(name)
        try:
            value = etcd_client.read(key).value
            response = flask.make_response(json.dumps(json.loads(value)))
        except etcd.EtcdKeyNotFound, e:
            response = flask.make_response(json.dumps({'kind': 'Status', 'code': 404}))

        return response

    def delete(self, name):
        key = '/paas/application_controllers/{}'.format(name)
        try:
            etcd_client.delete(key)
            response = flask.make_response(json.dumps({'kind': 'Status', 'code': 200}))
        except etcd.EtcdKeyNotFound, e:
            response = flask.make_response(json.dumps({'kind': 'Status', 'code': 404}))

        return response

    def put(self, name):
        template = request.get_json()
        if not _is_template_valid(template):
            response = flask.make_response(json.dumps({'kind': 'Status', 'code': 400}))
            return response

        key = '/paas/application_controllers/{}'.format(name)
        try:
            value = etcd_client.read(key).value
        except etcd.EtcdKeyNotFound, e:
            response = flask.make_response(json.dumps({'kind': 'Status', 'code': 404}))
            return response

        controller = json.loads(value)
        if controller['name'] != template['name']:
            response = flask.make_response(json.dumps({'kind': 'Status', 'code': 400}))
            return response

        etcd_client.write(key, json.dumps(template))
        response = flask.make_response(json.dumps({'kind': 'Status', 'code': 200}))
        return response

