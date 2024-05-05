#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : role
# author : ly_13
# date : 6/19/2023
import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet
from common.core.modelset import BaseModelSet
from system.models import UserRole
from system.utils.serializer import RoleSerializer, ListRoleSerializer

logger = logging.getLogger(__name__)


class RoleFilter(BaseFilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')

    class Meta:
        model = UserRole
        fields = ['name', 'code', 'is_active', 'description']


class RoleView(BaseModelSet):
    """角色管理"""
    queryset = UserRole.objects.all()
    serializer_class = RoleSerializer
    list_serializer_class = ListRoleSerializer
    ordering_fields = ['updated_time', 'name', 'created_time']
    filterset_class = RoleFilter
