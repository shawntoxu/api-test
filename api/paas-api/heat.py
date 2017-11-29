from keystoneclient.v2_0 import client as keystone_client
import heatclient.client
from heatclient.exc import *
import heatclient
import config
import time
from log import LOG

class HeatClient:
    def __init__(self):
        self.__heat_client = None
        self.token_expires = None
        self.token = None

    def _is_token_expired(self):
        if self.token is None:
            return True
        cur_time = time.gmtime()
        if time.mktime(self.token_expires) - time.mktime(cur_time) < 600:
            return True
        return False

    def __get_heat_client(self):
        if self.__heat_client is None or self.token_expires is None or self.token is None or self._is_token_expired():
            keystone = keystone_client.Client(username=config.HEAT_USERNAME, password=config.HEAT_PASSWORD, tenant_name=config.HEAT_USERNAME, auth_url=config.HEAT_AUTH_URL)
            self.token = keystone.auth_ref['token']['id']
            tenant = keystone.auth_ref['token']['tenant']['id']
            self.token_expires = time.strptime(keystone.auth_ref['token']['expires'], '%Y-%m-%dT%H:%M:%SZ')
            self.__heat_client = heatclient.client.Client('1', endpoint='http://{}:8004/v1/{}'.format(config.HEAT_IP, tenant), token=self.token)
        return self.__heat_client

    def create_stack(self, name, template):
        heat_client = self.__get_heat_client()

        fields = {
            'stack_name': name,
            'disable_rollback': True,
            'template': template,
            'timeout_mins': 60
        }
        try:
            heat_client.stacks.create(**fields)
        except Exception as e:
            LOG.error(e)
            raise e

    def get_stack(self, name):
        heat_client = self.__get_heat_client()
        for i in range(5):
            try:
                stack = heat_client.stacks.get(name)
                return stack
            except HTTPNotFound as e:
                raise
            except Exception as e:
                LOG.error('Failed to get stack <{}>'.format(name))
                LOG.error(type(e))
                if 'Timed out waiting for a reply to message ID' in str(e):
                    LOG.warning('Timed out getting stack <{}>. retry {}'.format(name, i))
                    time.sleep(2)
                else:
                    raise

    def get_stack_list(self):
        stacks = []
        heat_client = self.__get_heat_client()
        page =  heat_client.stacks.list(limit=0)
        while(True):
            try:
                stack = page.next()
                stacks.append(stack)
            except:
                break

        return stacks

    def get_resource_list(self, stack_name):
        heat_client = self.__get_heat_client()
        for i in range(5):
            try:
                return heat_client.resources.list(stack_name)
            except Exception as e:
                LOG.error('Failed to get resource list of stack <{}>'.format(stack_name))
                if 'Timed out waiting for a reply to message ID' in str(e):
                    LOG.warning('Timed out get resource list for stack <{}>'.format(stack_name))
                    time.sleep(2)
                else:
                    raise

    def is_stack_existed(self, stack_name):
        stack = None
        try:
            stack = self.get_stack(stack_name)
        except HTTPNotFound as e:
            pass
        except:
            raise
        
        return True if stack is not None else False

    def update_stack(self, stack_name, template):
        fields = {
            'stack_name': stack_name,
            'disable_rollback': True,
            'template': template,
            'timeout_mins': 60
        }
        try:
            heat_client = self.__get_heat_client()
            heat_client.stacks.update(stack_name, **fields)
        except Exception as e:
            LOG.error(str(e))
            raise e

    def delete_stack(self, stack_name):
        heat_client = self.__get_heat_client()
        heat_client.stacks.delete(stack_name)

    def cancel_update(self, stack_name):
        heat_client = self.__get_heat_client()
        heat_client.actions.cancel_update(stack_name)

    def get_stack_template(self, stack_name):
        heat_client = self.__get_heat_client()
        return heat_client.stacks.template(stack_name)

heat_client = HeatClient()

