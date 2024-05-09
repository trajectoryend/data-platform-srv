import hashlib
import random
import time
import requests

from server.config import WORKFLOW_URL, WORKFLOW_APPNAME, WORKFLOW_TOKEN
from workflow.models import FieldRow, FieldTab


def deal_custom_field(workflow_id, field_list):
    field_list_obj = []
    field_row = FieldRow.objects.filter(to_field_tab__to_workflow__workflow_id=int(workflow_id), is_active=True)


    if field_row.exists():
        for j in field_row:
            field_list_obj.append({
                'id': j.to_field_tab_id,
                'name': j.to_field_tab.name,
                'field_row_list': [
                    {
                        'id': j.id,
                        'name': j.name,
                        'field_list': []
                    }
                ]
            })
        none_row_list = []
        for i in field_list:

            i['field_col'] = random.randint(8, 12)
            if i.get('label', {}).get('field_row', '') == '':
                none_row_list.append(i)

        if len(none_row_list):
            field_list_obj.append({
                'id': '',
                'name': '其他信息',
                'field_row_list': [
                    {
                        'id': '',
                        'name': '其他行',
                        'field_list': none_row_list
                    }
                ]
            })

    return field_list_obj


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
        ticket = requests.get(
            url=self.workflow_url + '/api/v1.0/tickets/{ticket_id}'.format(ticket_id=ticket_id),
            headers=self.get_headers(username),
        )
        transition = requests.get(
            url=self.workflow_url + '/api/v1.0/tickets/{ticket_id}/transitions'.format(ticket_id=ticket_id),
            headers=self.get_headers(username),
        )

        if ticket.json().get('code') != 0:
            raise Exception(ticket.json().get('msg'))
        ticket_data = ticket.json().get('data', {'value': {}}).get('value', {})

        ticket_data['field_list'] = deal_custom_field(
            ticket_data.get('workflow_id', 0), ticket_data.get('field_list', [])
        )

        if transition.json().get('code') != 0:
            raise Exception(transition.json().get('msg'))
        transition_data = transition.json().get('data', {'value': []}).get('value', [])

        # 判断是否接单状态
        ticket_data['is_accept_status'] = False
        for i in transition_data:
            if i.get('is_accept', False):
                ticket_data['is_accept_status'] = True
                break

        # 判断当前状态是否可以进入加签状态
        ticket_data['can_add_node'] = bool(len(transition_data))

        ticket_data['transition'] = transition.json().get('data', {'value': []}).get('value', [])
        return ticket_data

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
