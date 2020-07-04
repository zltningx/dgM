# -*- coding: utf-8 -*-
# author: zltningx

from django.db import models
from apps.backend.models import User


class PenetrationTestTicket(models.Model):
    START, REVIEW, TESTING, COMPLETED = 0, 1, 2, 3
    STATUS = (
        (START, "草稿"),
        (REVIEW, "审核并分配测试人员"),
        (TESTING, "测试中"),
        (COMPLETED, "测试完成")
    )
    PRIORITIES = (
        (3, "P0"),
        (2, "P1"),
        (1, "P2"),
    )

    status = models.IntegerField("状态", choices=STATUS, default=START)
    title = models.CharField("标题", max_length=128)
    priority = models.IntegerField("优先级", choices=PRIORITIES, default=1)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    department = models.CharField("业务线(部门)", max_length=28, blank=True, null=False)
    dead_line = models.DateTimeField("期望最晚完成时间")
    description = models.TextField("描述", default="请输入测试域名、测试账号和其它必要测试信息 以供安全测试")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    transactors = models.ManyToManyField(User, related_name='transactors', blank=True)  # 审核人员


class PenetrationTestTicketResult(models.Model):
    penetration_test_ticket = models.OneToOneField(PenetrationTestTicket,
                                                   on_delete=models.CASCADE, related_name="ticket_result")
    tester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tester', blank=True, null=False)
    result_description = models.TextField("渗透结果描述", default="描述测试的结果", blank=True, null=False)


class PenetrationTestTicketSubWorkflow(models.Model):
    penetration_test_ticket = models.ForeignKey(PenetrationTestTicket,
                                                on_delete=models.CASCADE,
                                                related_name='sub_workflow')
    transactor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pt_transactor')
    action = models.CharField("操作", max_length=10)
    workflow_description = models.TextField("处理意见", blank=True, null=False, default="无")
    update_time = models.DateTimeField("更新时间", auto_now_add=True)
