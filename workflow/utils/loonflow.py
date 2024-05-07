import hashlib
import time
import requests

from server.config import WORKFLOW_URL, WORKFLOW_APPNAME, WORKFLOW_TOKEN


class Loonflow(object):

    def __init__(self, workflow_url, workflow_appname, workflow_token):
        self.workflow_appname = workflow_appname
        self.workflow_token = workflow_token
        self.workflow_url = workflow_url

    def get_headers(self, username):
        timestamp = str(time.time())[:10]
        ori_str = timestamp + self.workflow_token
        signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        return dict(signature=signature, timestamp=timestamp, appname=self.workflow_appname, username=username)

    def get_workflows_custom_fields(self, workflow_id, username='admin'):
        params = dict(per_page=1000, page=1)
        r = requests.get(
            url=self.workflow_url + '/api/v1.0/workflows/{}/custom_fields'.format(str(workflow_id)),
            headers=self.get_headers(username),
            params=params
        )
        print(r.json())
        if r.json().get('code') != 0:
            raise Exception(r.json().get('message'))
        return r.json().get('data').get('value')

    def get_tickets_list(self, params, username):
        r = requests.get(
            url=self.workflow_url + '/api/v1.0/tickets',
            headers=self.get_headers(username),
            params=params
        )
        if r.json().get('code') != 0:
            raise Exception(r.json().get('message'))
        return r.json().get('data')


loonflow = Loonflow(WORKFLOW_URL, WORKFLOW_APPNAME, WORKFLOW_TOKEN)
print(loonflow.get_tickets_list({'category': 'all'}, username='admin'))
