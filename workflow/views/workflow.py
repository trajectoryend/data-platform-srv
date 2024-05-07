import logging

from rest_framework import viewsets

from common.core.modelset import BaseModelSet
from common.core.permission import IsAuthenticated
from common.core.response import ApiResponse
from workflow.models import WorkflowType
from workflow.utils.filter import WorkflowTypeFilter
from workflow.utils.serializer import WorkflowTypeSerializer, ListWorkflowTypeSerializer
from workflow.utils.loonflow import loonflow

logger = logging.getLogger(__name__)


class WorkflowTypeView(BaseModelSet):
    """工作流类型管理"""
    queryset = WorkflowType.objects.filter(is_active=True)
    serializer_class = WorkflowTypeSerializer
    list_serializer_class = ListWorkflowTypeSerializer
    ordering_fields = ['-order_id']
    filterset_class = WorkflowTypeFilter


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
