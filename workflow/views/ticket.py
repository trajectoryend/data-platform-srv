import logging

from rest_framework import viewsets


from common.core.permission import IsAuthenticated
from common.core.response import ApiResponse
from workflow.utils.loonflow import loonflow

logger = logging.getLogger(__name__)


def generate_search_dict(search_json):
    search_dict = dict()
    search_dict['page'] = search_json.get('page', 1)
    search_dict['per_page'] = search_json.get('per_page', 20)
    search_dict['category'] = search_json.get('category', 'all')

    for i in search_json.get("data", []):
        if i['key'] == 'gmt_created':
            search_dict['create_start'] = i['value'][0]
            search_dict['create_end'] = i['value'][0]
        else:
            search_dict[i['key']] = i['value']
    return search_dict


class SearchTicketView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request_data = self.request.data
        data = loonflow.list_ticket(generate_search_dict(request_data), self.request.user.username)
        return ApiResponse(data=data)


class TicketView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request_data = self.request.data
        data = loonflow.create_ticket(request_data, self.request.user.username)
        return ApiResponse(data=data)

    def retrieve(self, request, pk=None):
        data = loonflow.retrieve_ticket(str(pk), self.request.user.username)
        return ApiResponse(data=data)

    def patch(self, request, pk=None):
        data = loonflow.patch_ticket(str(pk), self.request.data, self.request.user.username)
        return ApiResponse(data=data)


class TicketTransitionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        params = self.request.query_params
        ticket_id = params.get('ticket_id', None)
        if ticket_id:
            data = loonflow.list_ticket_transition(ticket_id, request.user.username)
            return ApiResponse(data=data)
        return ApiResponse(code=1001, status=400, detail="参数错误")


class TicketFlowlogView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        params = self.request.query_params
        ticket_id = params.get('ticket_id', None)
        if ticket_id:
            data = loonflow.list_ticket_flowlog(ticket_id, params, request.user.username)
            return ApiResponse(data=data)
        return ApiResponse(code=1001, status=400, detail="参数错误")
