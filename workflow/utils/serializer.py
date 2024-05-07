from rest_framework.serializers import ModelSerializer

from workflow import models


class WorkflowTypeSerializer(ModelSerializer):
    class Meta:
        model = models.WorkflowType
        fields = ['pk', 'name', 'order_id', 'is_active']
        read_only_fields = ['pk']


class ListWorkflowTypeSerializer(ModelSerializer):
    class Meta:
        model = models.WorkflowType
        fields = ['pk', 'name']
        read_only_fields = ['pk']
