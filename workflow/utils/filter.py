
from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet
from workflow.models import WorkflowType, Workflow, View


class WorkflowTypeFilter(BaseFilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = WorkflowType
        fields = ['name']


class WorkflowFilter(BaseFilterSet):

    class Meta:
        model = Workflow
        fields = ['to_workflow_type']


class ViewFilter(BaseFilterSet):

    class Meta:
        model = View
        fields = ['to_workflow']
