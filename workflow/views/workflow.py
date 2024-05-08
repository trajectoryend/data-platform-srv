import logging

from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from common.core.modelset import BaseAction
from common.core.pagination import DynamicPageNumber
from common.core.permission import IsAuthenticated
from common.core.response import ApiResponse
from workflow.models import WorkflowType, Workflow, View
from workflow.utils.filter import WorkflowTypeFilter, WorkflowFilter, ViewFilter
from workflow.utils.serializer import ListWorkflowTypeSerializer, ListWorkflowSerializer, ListViewSerializer, \
    RetrieveViewSerializer, SelectViewSerializer
from workflow.utils.loonflow import loonflow

logger = logging.getLogger(__name__)


class WorkflowTypeView(BaseAction, mixins.ListModelMixin, GenericViewSet):
    """工作流类型管理"""
    queryset = WorkflowType.objects.filter(is_active=True)
    serializer_class = ListWorkflowTypeSerializer
    ordering_fields = ['-order_id']
    pagination_class = DynamicPageNumber(1000)
    filterset_class = WorkflowTypeFilter


class WorkflowView(BaseAction, mixins.ListModelMixin, GenericViewSet):
    """工作流管理"""
    queryset = Workflow.objects.filter(is_active=True)
    serializer_class = ListWorkflowSerializer
    ordering_fields = ['-order_id']
    pagination_class = DynamicPageNumber(1000)
    filterset_class = WorkflowFilter


class ViewView(BaseAction, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """工作流视图管理"""
    queryset = View.objects.filter(is_active=True)
    serializer_class = ListViewSerializer
    ordering_fields = ['-order_id']
    pagination_class = DynamicPageNumber(1000)
    filterset_class = ViewFilter

    def get_serializer_class(self):
        if self.action == 'list':
            if self.request.query_params.get('page_size', '20') == str(100000):
                return SelectViewSerializer
            else:
                return ListViewSerializer
        elif self.action == 'retrieve':
            return RetrieveViewSerializer
        return RetrieveViewSerializer


class WorkflowCustomFieldView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        params = self.request.query_params
        workflow_id = params.get('workflow_id', None)
        if workflow_id:
            data = loonflow.list_workflow_custom_field(workflow_id, request.user.username)
            return ApiResponse(data=data)
        return ApiResponse(code=1001, status=400, detail="参数错误")


class WorkflowInitStateView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        params = self.request.query_params
        workflow_id = params.get('workflow_id', None)
        if workflow_id:
            data = loonflow.get_workflow_init_state(workflow_id, request.user.username)
            return ApiResponse(data=data)
        return ApiResponse(code=1001, status=400, detail="参数错误")
