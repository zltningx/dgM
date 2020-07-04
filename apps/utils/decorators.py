# -*- coding: utf-8 -*-
# author: zltningx

from django.http.response import HttpResponseBase
from rest_framework.response import Response
from apps.utils.xss_filter import json_xss_filter

import json


def make_response(func_or_view_class):
    """
    this decorator can be used in django view class or the function of view class
    :param func_or_view_class:
    :return:
    """
    if type(func_or_view_class) is type:
        super_finalize_response = func_or_view_class.finalize_response

        def finalize_response(self, request, response, *args, **kwargs):
            if not isinstance(response, HttpResponseBase):
                response = Response(response)
            return super_finalize_response(self, request, response, *args, **kwargs)
        func_or_view_class.finalize_response = finalize_response
        return func_or_view_class
    else:
        func = func_or_view_class

        def func_decorator(*args, **kwargs):
            resp = func(*args, **kwargs)
            if not isinstance(resp, HttpResponseBase):
                return Response(resp)
            else:
                return resp
        return func_decorator


def xss_filter(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result.content = result.content
        try:
            jsondata = json.loads(result.content)
            result.content = json.dumps(json_xss_filter(jsondata))
        except:
            result.content = json_xss_filter(result.content)
        return result
    return wrapper
