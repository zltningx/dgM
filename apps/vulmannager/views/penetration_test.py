# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.vulmannager.filters import IsOwnerOrAdminOrTransactorsFilterBackend
from apps.vulmannager.models import (
    PenetrationTestTicket, PenetrationTestTicketResult,
    PenetrationTestTicketSubWorkflow, Vulnerability)
from apps.vulmannager.serializers import (
    PenetrationTestTicketSerializer, PenetrationTestTicketResultSerializer,
    PenetrationTestTicketSubWorkflowSerializer)
from apps.utils.pagination import MyPageNumberPagination
from apps.vulmannager.permissions import TicketIsOwnerOrReadOnly
from apps.utils.decorators import make_response
from apps.backend.http import ResponseBody, code


class PenetrationTestViewSet(ModelViewSet):
    permission_classes = [TicketIsOwnerOrReadOnly]
    serializer_class = PenetrationTestTicketSerializer
    pagination_class = MyPageNumberPagination
    queryset = PenetrationTestTicket.objects.all()
    filter_backends = [IsOwnerOrAdminOrTransactorsFilterBackend,
                       DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status']
    ordering_fields = ['id', 'create_time', 'dead_line']
    search_fields = ['title', 'creator__full_name', 'department']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PenetrationTestTicketResultViewSet(ModelViewSet):
    serializer_class = PenetrationTestTicketResultSerializer
    pagination_class = MyPageNumberPagination
    queryset = PenetrationTestTicketResult.objects.all()


class PenetrationTestTicketSubWorkflowViewSet(ModelViewSet):
    serializer_class = PenetrationTestTicketSubWorkflowSerializer
    pagination_class = MyPageNumberPagination
    queryset = PenetrationTestTicketSubWorkflow.objects.all()


@make_response
class PenetrationTestTicketManager(ViewSet):
    @action(methods=['get'], detail=False, url_path='get_types')
    def get_types(self, request, *args, **kwargs):
        resp = ResponseBody()
        data = Vulnerability.VUL_TYPES
        resp.code = code.success
        resp.data = data
        return resp
