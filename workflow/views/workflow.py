import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet
from common.core.modelset import BaseModelSet
from workflow.models import WorkflowType
from workflow.utils.serializer import WorkflowTypeSerializer, ListWorkflowTypeSerializer

logger = logging.getLogger(__name__)


class WorkflowTypeFilter(BaseFilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = WorkflowType
        fields = ['name']


class WorkflowTypeView(BaseModelSet):
    """工作流类型管理"""
    queryset = WorkflowType.objects.filter(is_active=True)
    serializer_class = WorkflowTypeSerializer
    list_serializer_class = ListWorkflowTypeSerializer
    ordering_fields = ['order_id']
    filterset_class = WorkflowTypeFilter
