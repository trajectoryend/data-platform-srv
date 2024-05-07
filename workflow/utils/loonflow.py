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

    def list_workflow_custom_field(self, workflow_id, username='admin'):
        r = requests.get(
            url=self.workflow_url + '/api/v1.0/workflows/{workflow_id}/custom_fields'.format(
                workflow_id=str(workflow_id)
            ),
            headers=self.get_headers(username),
            params=dict(per_page=1000, page=1)
        )
        if r.json().get('code') != 0:
            raise Exception(r.json().get('msg'))
        return r.json().get('data').get('value')

    def list_ticket(self, params, username):
        r = requests.get(
            url=self.workflow_url + '/api/v1.0/tickets',
            headers=self.get_headers(username),
            params=params
        )
        if r.json().get('code') != 0:
            raise Exception(r.json().get('msg'))
        return r.json().get('data')

    def create_ticket(self, data, username):
        r = requests.post(
            url=self.workflow_url + '/api/v1.0/tickets',
            headers=self.get_headers(username),
            data=data
        )
        if r.json().get('code') != 0:
            raise Exception(r.json().get('msg'))
        return r.json().get('data')

    def retrieve_ticket(self, ticket_id, username):
        r = requests.get(
            url=self.workflow_url + '/api/v1.0/tickets/{ticket_id}'.format(ticket_id=ticket_id),
            headers=self.get_headers(username),
        )
        if r.json().get('code') != 0:
            raise Exception(r.json().get('msg'))
        return r.json().get('data')

    def patch_ticket(self, ticket_id, data, username):
        r = requests.patch(
            url=self.workflow_url + '/api/v1.0/tickets/{ticket_id}'.format(ticket_id=ticket_id),
            headers=self.get_headers(username),
            data=data
        )
        if r.json().get('code') != 0:
            raise Exception(r.json().get('msg'))
        return r.json().get('data')

    def list_ticket_transition(self, ticket_id, username):
        r = requests.get(
            url=self.workflow_url + '/api/v1.0/tickets/{ticket_id}/transitions'.format(ticket_id=ticket_id),
            headers=self.get_headers(username),
        )
        if r.json().get('code') != 0:
            raise Exception(r.json().get('msg'))
        return r.json().get('data')

    def list_ticket_flowlog(self, ticket_id, params, username):
        r = requests.get(
            url=self.workflow_url + '/api/v1.0/tickets/{ticket_id}/flowlogs'.format(ticket_id=ticket_id),
            headers=self.get_headers(username),
            params=params
        )
        if r.json().get('code') != 0:
            raise Exception(r.json().get('msg'))
        return r.json().get('data')

    def get_workflow_init_state(self, workflow_id, username):
        r = requests.get(
            url=self.workflow_url + '/api/v1.0/workflows/{workflow_id}/init_state'.format(
                workflow_id=str(workflow_id)
            ),
            headers=self.get_headers(username),
        )
        if r.json().get('code') != 0:
            raise Exception(r.json().get('msg'))
        return r.json().get('data')


loonflow = Loonflow(WORKFLOW_URL, WORKFLOW_APPNAME, WORKFLOW_TOKEN)
