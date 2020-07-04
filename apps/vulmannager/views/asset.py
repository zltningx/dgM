# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.vulmannager.serializers import AssetSerializer, PortSerializer
from apps.vulmannager.permissions import AdminOrReadOnly
from apps.vulmannager.models import Asset, Port
from apps.utils.pagination import MyPageNumberPagination


class AssetViewSet(ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    serializer_class = AssetSerializer
    pagination_class = MyPageNumberPagination
    queryset = Asset.objects.all()
    filter_backends = [OrderingFilter, SearchFilter]
    # filterset_fields = ['status']
    ordering_fields = ['id', 'create_time', 'update_time']
    search_fields = ['ip', 'name', 'domain']


class PortViewSet(ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    serializer_class = PortSerializer
    pagination_class = MyPageNumberPagination
    queryset = Port.objects.all()
    # filter_backends = [OrderingFilter, SearchFilter]
