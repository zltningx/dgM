# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class IsOwnerOrAdminOrTransactorsFilterBackend(BaseFilterBackend):
    """
    Filter that only allows Owner|Admin|Transactors to see this objects.
    """
    def filter_queryset(self, request, queryset, view):
        if request.query_params.__contains__('type'):
            if request.query_params['type'] == 'own':
                return queryset.filter(creator=request.user).distinct()
            if request.query_params['type'] == 'todo':
                return queryset.filter(Q(transactors__in=[request.user]) & ~Q(status=3)).distinct()
        if request.user.is_superuser or request.user.groups.filter(name='审核组'):
            return queryset
        # distinct 消除重复行 神秘事件
        return queryset.filter(Q(creator=request.user) | Q(transactors__in=[request.user])).distinct()


class VulWorkflowFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.query_params.__contains__('type') and request.query_params['type'] == 'own':
            return queryset.filter(Q(vulnerability__reporter=request.user)).distinct()
        return queryset


class StatusFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.query_params.__contains__('status'):
            if '-' in request.query_params['status']:
                return queryset.filter(~Q(status=request.query_params['status'])).distinct()
        return queryset
