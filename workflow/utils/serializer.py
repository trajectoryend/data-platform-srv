import json

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from workflow import models


class ListWorkflowTypeSerializer(ModelSerializer):
    class Meta:
        model = models.WorkflowType
        fields = ['pk', 'name']
        read_only_fields = ['pk']


class ListWorkflowSerializer(ModelSerializer):
    class Meta:
        model = models.Workflow
        fields = ['pk', 'name', 'workflow_id']


class ListViewSerializer(ModelSerializer):
    class Meta:
        model = models.View
        fields = ['pk', 'name']


class SelectViewSerializer(ModelSerializer):
    class Meta:
        model = models.View
        fields = ['pk', 'name']


class RetrieveViewSerializer(ModelSerializer):

    search_params = serializers.SerializerMethodField()
    table_column = serializers.SerializerMethodField()

    class Meta:
        model = models.View
        fields = ['pk', 'name', 'view_type', 'search_mode', 'search_params', 'table_column', 'order_field',
                  'order_type']

    def get_search_params(self, obj):
        return json.loads(obj.search_params) if obj.search_params else {}

    def get_table_column(self, obj):
        return json.loads(obj.table_column) if obj.table_column else []
