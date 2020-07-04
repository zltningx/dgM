# -*- coding: utf-8 -*-
# author: zltningx

from apps.backend.http import code


class ResponseBody(dict):
    def __init__(self, seq=None, **kwargs):
        super(ResponseBody, self).__init__(**kwargs)
        self['code'] = 200
        self['data'] = {}
        self['msg'] = 'success'

    @property
    def code(self):
        return self['code']

    @code.setter
    def code(self, value):
        self['code'] = value
        if code.has_code(value):
            self['msg'] = str(value)

    @property
    def data(self):
        return self['data']

    @data.setter
    def data(self, value):
        self['data'] = value

    @property
    def msg(self):
        return self['msg']

    @msg.setter
    def msg(self, value):
        self['msg'] = value
