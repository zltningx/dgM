# -*- coding: utf-8 -*-
# author: zltningx


class StatusCode(int):

    def __str__(self):
        if has_code(self):
            return _code_to_message[self]
        else:
            return str(unknown_error)


def has_code(code):
    return code in _code_to_message


success = StatusCode(200)
unknown_error = StatusCode(501)
internal_error = StatusCode(502)
param_missing = StatusCode(408)
param_illegal = StatusCode(409)
invalid_data = StatusCode(410)
biz_error = StatusCode(503)

# # email: 500 ~ 999
# email_already_exists = StatusCode(500)
# email_not_exists = StatusCode(501)
#
# # ldap: 1000 ~ 1499
# ldap_error = StatusCode(1000)
#
# # account - user
# #   - user: 20000 ~ 20499
# user_interval_error = StatusCode(20000)
# user_is_not_exists = StatusCode(20001)
# user_is_not_ops_operator = StatusCode(20002)
#
# #   - dingtalk: 21000 ~ 21499
# dingtalk_interval_error = StatusCode(21000)
# dingtalk_get_auth_code_error = StatusCode(21001)
#
# # execute sql: 21500 ~ 21999
# execute_sql_error = StatusCode(21500)
#
# # ansible  22000 ~ 22499
# ansible_execute_command_error = StatusCode(22000)
#
# # supervisor 22500 ~ 22999
# supervisor_error = StatusCode(22500)
#
# # qd auth
# qdauth_error = StatusCode(23000)
#
# # wiki jira
# wiki_jira_error = StatusCode(23500)
#
# # jumpserver
# jumpserver_error = StatusCode(24000)
#
# # laifenqi
# laifenqi_auth_error = StatusCode(24500)
#
# # bi dt
# bi_dt_error = StatusCode(25000)
#
# # dashboard grafana api
# grafana_error = StatusCode(25500)
#
# # config center
# config_center_diff_error = StatusCode(25500)
#
# # query sql 数据查询
# query_sql_log_does_not_exist = StatusCode(25600)
# query_sql_session_not_exist = StatusCode(25601)
#
# # autosql sql上线
# auto_sql_merge_alter = StatusCode(25701)

_code_to_message = {
    success: 'success',
    internal_error: 'internal error',
    param_missing: 'param missing',
    param_illegal: 'param illegal',
    unknown_error: 'unknown error',
    invalid_data: 'invalid data',
    biz_error: "biz error",
    #
    # email_already_exists: '该用户已经注册',
    # email_not_exists: 'email address does not exist',
    #
    # ldap_error: 'failed ldap operations',
    #
    # user_interval_error: 'interval user error',
    # user_is_not_exists: 'user is not exists',
    #
    # dingtalk_interval_error: 'interval dingtalk error',
    #
    # user_is_not_ops_operator: '不是运维操作人员',
    #
    # ansible_execute_command_error: 'ansible 执行命令返回失败结果',
    #
    # supervisor_error: 'supervisor error',
    #
    # qdauth_error: 'failed to call qd auth api',
    #
    # wiki_jira_error: 'failed to call wiki jira api',
    #
    # jumpserver_error: 'failed to call jumpserver api',
    #
    # laifenqi_auth_error: 'failed to call laifenqi auth api',
    #
    # bi_dt_error: 'failed to call bi dt api',
    #
    # dingtalk_get_auth_code_error: 'failed to get auth code from dingtalk',
    #
    # config_center_diff_error: '配置文件内容不一致',
    # # query sql
    # query_sql_log_does_not_exist: '该查询已经完成或者不存在！',
    # query_sql_session_not_exist: '该查询已经完成!',
    # auto_sql_merge_alter: '一张表的多剧alter语句，请合并成一条。或联系dba处理'

}
