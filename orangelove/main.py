# -*-coding:utf-8-*-

import traceback
import time
import asyncio

import uvicorn
import redis
from fastapi import FastAPI, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from orangelove.routers.common import common_router
from orangelove.common.utils.fastapi_tools import get_body
from orangelove.common.log import logger, error_logger


def create_app():
    app = FastAPI()
    # 注册路由
    app.include_router(common_router)
    # app.include_router(image_router)
    # app.include_router(inner_router)
    # redis
    # rds = redis.StrictRedis(host=Config.rds_host, port=Config.rds_port,
    #                         password=Config.rds_password, db=Config.rds_db,
    #                         decode_responses=True)
    # db
    # session = new_session_factory(Config.db_url, pool_recycle=Config.db_pool_recycle)
    # db = session()
    # # check db
    return app


app = create_app()


# @app.exception_handler(IntegrityError)  # db异常
# async def wf_exception_handle(request: Request, exc: IntegrityError):
#     """
#
#     :param request: 请求
#     :param exc: 错误类
#     :return:
#     """
#     try:
#         body = await get_body(request)
#     except Exception as e:
#         body = '[get body error]'
#     logger.error(
#         'sqlalchemy.exc.IntegrityError:\n{}\nurl:{}\nheaders:\n{}\nbody:\n{}'.format(str(exc), request.url,
#                                                                                      request.headers, body))
#     error_logger.error(
#         'sqlalchemy.exc.IntegrityError:\n{}\nurl:{}\nheaders:\n{}\nbody:\n{}'.format(str(exc), request.url,
#                                                                                      request.headers, body))
#
#     try:
#         G.db.rollback()
#     except Exception as e:
#         logger.warning(e)
#
#     return JSONResponse({'code': exc.code, 'msg': 'db error:{}'.format(str(exc))}, status_code=500)
#
#
# @app.exception_handler(WFNotebookError)  # 自定义异常
# async def wf_exception_handle(request: Request, exc: WFNotebookError):
#     """
#
#     :param request: 请求
#     :param exc: 错误类
#     :return:
#     """
#     if exc.code in [AppCode.Forbidden, AppCode.Not_Found, AppCode.Method_Not_Allowed]:
#         logger.error('\nWFNotebookError:{},url:{}'.format(exc.msg, request.url))
#         error_logger.error('\nWFNotebookError:{},url:{}'.format(exc.msg, request.url))
#         return JSONResponse({'code': exc.code, 'msg': exc.msg, 'data': exc.data}, status_code=exc.status_code)
#     try:
#         body = await get_body(request)
#     except Exception as e:
#         body = '[get body error]'
#     error_logger.error(
#         'status_code:{}\ncode:{}\nWFNotebookError:\n{}\nurl:{}\nheaders:\n{}\nbody:\n{}'.format(exc.status_code,
#                                                                                                 exc.code, exc.msg,
#                                                                                                 request.url,
#                                                                                                 request.headers,
#                                                                                                 body))
#     logger.error(
#         'status_code:{}\ncode:{}\nWFNotebookError:\n{}\nurl:{}\nheaders:\n{}\nbody:\n{}'.format(exc.status_code,
#                                                                                                 exc.code, exc.msg,
#                                                                                                 request.url,
#                                                                                                 request.headers,
#                                                                                                 body))
#     return JSONResponse({'code': exc.code, 'msg': exc.msg, 'data': exc.data}, status_code=exc.status_code)
#
#
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """计时"""
    start_time = time.time()
    logger.info('request url:{} from host:{}'.format(request.url, request.headers.get('host')))
    body = await get_body(request)
    try:
        response = await call_next(request)
    except Exception as exc:
        response = JSONResponse(
            status_code=200,
            content=jsonable_encoder({
                "code": 110,
                "msg": "系统错误 System error",
            })
        )
        logger.error(
            '\n系统错误 System error:\n{}\nurl:{}\nheaders:\n{}\nbody:\n{}\ntraceback:{}'.format(str(exc), request.url,
                                                                                                 request.headers,
                                                                                                 body,
                                                                                                 traceback.format_exc()))
        error_logger.error(
            '\n系统错误 System error:\n{}\nurl:{}\nheaders:\n{}\nbody:\n{}\ntraceback:{}'.format(str(exc), request.url,
                                                                                                 request.headers,
                                                                                                 body,
                                                                                                 traceback.format_exc()))

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


def main(debug=False):
    if debug:
        print('=============dev debug============')
        uvicorn.run('main:app', host='0.0.0.0', port=5001, reload=True, loop='uvloop')
    else:
        uvicorn.run(app, host='0.0.0.0', port=5001, reload=False, loop='uvloop')


if __name__ == '__main__':
    main(debug=True)
