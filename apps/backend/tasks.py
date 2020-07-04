# -*- coding: utf-8 -*-
# author: zltningx

from typing import List
from jinja2 import Environment, PackageLoader
from celery import shared_task

from apps.utils.email import send_dragon_m_email
from apps.backend.models import SMTPConfig
from apps.vulmannager.models import VulWorkflow

jinja_env = Environment(loader=PackageLoader('apps.backend', 'template'))


@shared_task
def send_smtp_test_email(to_addrs: List[str]):
    # 用于测试SMTP配置项
    smtp_config = SMTPConfig.objects.all().first()
    if not smtp_config:
        raise Exception("DragonM安全平台还未配置SMTP")
    template = jinja_env.get_template('test_smtp_config.html')
    render_result = template.render(signature=smtp_config.signature)
    # from_addr 目前先用这SMTPConfig.username
    send_dragon_m_email(
        smtp_host=smtp_config.server,
        smtp_port=smtp_config.port,
        smtp_username=smtp_config.username,
        smtp_password=smtp_config.password,
        smtp_encryption=smtp_config.encryption_method,
        from_addr=smtp_config.username,
        to_addrs=to_addrs,
        subject='SMTP配置成功',
        content=render_result
    )


@shared_task
def send_pen_todo_email(to_addrs: List[str], url: str, title: str, creator: str, message: str):
    smtp_config = SMTPConfig.objects.all().first()
    if not smtp_config:
        raise Exception("DragonM安全平台还未配置SMTP")
    template = jinja_env.get_template('send_pen_todo.html')
    render_result = template.render(
        url=url,
        title=title,
        creator=creator,
        message=message,
        signature=smtp_config.signature)
    send_dragon_m_email(
        smtp_host=smtp_config.server,
        smtp_port=smtp_config.port,
        smtp_username=smtp_config.username,
        smtp_password=smtp_config.password,
        smtp_encryption=smtp_config.encryption_method,
        from_addr=smtp_config.username,
        to_addrs=to_addrs,
        subject='待办安全工单提醒',
        content=render_result
    )


@shared_task
def send_vul_todo_email(to_addrs: List[str], obj: VulWorkflow, link: str, message: str):
    print(to_addrs)
    smtp_config = SMTPConfig.objects.all().first()
    if not smtp_config:
        raise Exception("DragonM安全平台还未配置SMTP")
    template = jinja_env.get_template('send_vul_todo.html')
    # decode obj
    title = obj.title
    url = obj.vulnerability.url
    reporter = obj.vulnerability.reporter.full_name
    status = obj.vulnerability.get_status_display()
    rank = obj.vulnerability.get_rank_display()
    render_result = template.render(
        title=title,
        reporter=reporter,
        url=url,
        status=status,
        rank=rank,
        link=link,
        message=message,
        signature=smtp_config.signature)
    send_dragon_m_email(
        smtp_host=smtp_config.server,
        smtp_port=smtp_config.port,
        smtp_username=smtp_config.username,
        smtp_password=smtp_config.password,
        smtp_encryption=smtp_config.encryption_method,
        from_addr=smtp_config.username,
        to_addrs=to_addrs,
        subject='待办漏洞事项提醒',
        content=render_result
    )
