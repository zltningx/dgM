# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from apps.backend.http import ResponseBody, code
from apps.backend.permissions import IsSuperUser
from apps.utils.decorators import make_response
from apps.backend.tasks import send_smtp_test_email, send_pen_todo_email, send_vul_todo_email

from apps.vulmannager.models import PenetrationTestTicket
from apps.vulmannager.models import VulWorkflow


@make_response
class Notify(ViewSet):
    @action(methods=['post'], detail=False, url_path='test')
    def send_test_email(self, request, *args, **kwargs):
        data = request.data
        send_smtp_test_email.delay([data['email']])
        resp = ResponseBody()
        resp.data = [request.data]
        resp.code = code.success
        return resp

    @action(methods=['get'], detail=False, url_path='pen/todo')
    def send_pen_todo_email(self, request, *args, **kwargs):
        pen_id = request.query_params['id']
        obj = PenetrationTestTicket.objects.get(id=pen_id)
        message = ''
        if obj.status == 0:
            message = "您的工单被拒绝"
            to_addr = [obj.creator.email]
            url = f"http://{request.META['HTTP_HOST']}/#/tickets/own"
        else:
            to_addr = [user.email for user in obj.transactors.all()]
            url = f"http://{request.META['HTTP_HOST']}/#/tickets/todo"
        print(to_addr)
        send_pen_todo_email.delay(to_addr, url, obj.title, obj.creator.full_name, message)
        resp = ResponseBody()
        resp.data = obj.title
        resp.code = code.success
        return resp

    @action(methods=['get'], detail=False, url_path='vul/todo')
    def send_vul_todo_email(self, request, *args, **kwargs):
        vul_id = request.query_params['id']
        message = request.query_params['message']
        obj = VulWorkflow.objects.get(id=vul_id)
        if obj.vulnerability.status == 1:
            to_addr = [user.email for user in obj.asset.pics.all()]
        else:
            to_addr = [obj.vulnerability.reporter.email]
        vul_link = f"http://localhost:9528/#/vuls/workflow/{vul_id}"
        send_vul_todo_email.delay(to_addr, obj, vul_link, message)
        resp = ResponseBody()
        resp.data = obj.title
        resp.code = code.success
        return resp

