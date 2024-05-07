
from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet
from workflow.models import WorkflowType


class WorkflowTypeFilter(BaseFilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = WorkflowType
        fields = ['name']
