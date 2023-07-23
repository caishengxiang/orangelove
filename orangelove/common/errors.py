#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自定义错误类 与 错误状态码
"""


class HttpStatusCode:
    """http状态码"""
    OK = 200
    Bad_Request = 400
    Unauthorized = 401
    Forbidden = 403
    Not_Found = 404
    Method_Not_Allowed = 405
    Unprocessable_Entity = 422
    Locked = 423
    Too_Many_Requests = 429
    Internal_Server_Error = 500
    Not_Implemented = 501
    Service_Unavailable = 503


#  默认应用code信息
DEFAULT_APP_CODE_MSG = {
    0: 'OK',
    4423: 'git not commit',
    4424: 'CODE文件夹不存在，无法生成版本。是否自动生成CODE文件夹？',
    400: "客户端请求的语法错误，服务器无法理解",
    401: '用户未登陆/登陆失败',
    403: '权限不足',
    404: '找不到资源',
    405: '客户端请求中的API被禁止',
    422: "请求格式正确,但是由于含有语义错误,无法响应。",
    423: "当前资源被锁定,不能删改",
    429: "API访问次数超限",
    500: "服务器异常",
    501: '服务器不支持请求的功能，无法完成请求',
    503: '由于超载或系统维护，服务器暂时无法处理客户端的请求。',

    4001: '复制失败，总文件大小不能超过2GB，请在终端进行此操作',
    4002: '复制失败，总文件数不能超过2000个，请在终端进行此操作',
    4003: '移动失败，总文件大小不能超过5GB，请在终端进行此操作',
    4004: '移动失败，总文件数不能超过5000个，请在终端进行此操作',
    4005: '删除失败，总文件数不能超过5000个，请在终端进行此操作',
    4006: "token 校验不通过, 实验已经被打开",
    4007: "token 不存在，实验打开状态过期",
    4017: "文件保存中，请稍后重试",
    4425: '文件数量过多，不支持展开',
    4404: '文件(夹)不存在',
    8027: '全量作业运行数量已达到上限'
}


class AppCode:
    """应用状态码"""
    OK = 0
    GIT_NO_COMMIT = 4423
    GIT_NO_CODE_DIR = 4424

    Bad_Request = 400
    Unauthorized = 401
    Forbidden = 403
    Not_Found = 404
    Method_Not_Allowed = 405
    Unprocessable_Entity = 422
    Locked = 423
    Too_Many_Requests = 429
    Internal_Server_Error = 500
    Not_Implemented = 501
    Service_Unavailable = 503
    Token_Verification_Failed = 4006
    Token_Not_Found = 4007
    File_Open_Fail = 4017
    File_Not_Found = 4404
    ERR_NOTEBOOK_JOB_OVER_FLOW = 8027


class CustomError(Exception):
    """
    自定义异常类
    """

    def __init__(self, msg=None, code=AppCode.Internal_Server_Error, status_code=HttpStatusCode.OK, data=None):
        self.code = code
        self.status_code = status_code

        msg_head = DEFAULT_APP_CODE_MSG.get(code)
        if msg:
            # 有新提示, 覆盖原来的
            self.msg = '{msg}'.format(msg=msg)
        elif msg_head:
            self.msg = '{msg_head}'.format(msg_head=msg_head)
        else:
            self.msg = '未知错误'
        self.data = data

    def __str__(self):
        return self.msg
