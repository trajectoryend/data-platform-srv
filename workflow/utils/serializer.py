import json
import os.path

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from workflow import models


class WorkflowTypeSerializer(ModelSerializer):
    class Meta:
        model = models.WorkflowType
        fields = ['pk', 'name', 'icon', 'order_id', 'is_active']
        read_only_fields = ['pk']


class ListWorkflowTypeSerializer(ModelSerializer):
    class Meta:
        model = models.WorkflowType
        fields = ['pk', 'name']
        read_only_fields = ['pk']

