# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 100
