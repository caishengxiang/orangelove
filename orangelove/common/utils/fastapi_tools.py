# -*-coding:utf-8-*-
import json
import redis
from fastapi import Depends
from fastapi.requests import Request
from orangelove.common.errors import CustomError
# from orangelove.dbs.orm import new_session_factory
from orangelove.common.config import Config
from orangelove.common import G
from orangelove.common.log import logger, error_logger
from orangelove.common.classes import User
from fastapi.responses import JSONResponse


async def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


async def get_params(req: Request, data_format='json'):
    params = {}
    # query
    for key, value in req.query_params.multi_items():
        params[key] = value
    # body
    body = await get_body(request=req)
    if body:
        if data_format == 'json':
            data = await req.json()
            for key, value in data.items():
                params[key] = value
        elif data_format == 'form':
            form = await req.form()
            for key, value in form.multi_items():  # form.items()
                params[key] = value
    return params


def render(msg='ok', code=0, data=None, status_code=200):
    logger.info(str({'code': code, 'msg': msg, 'data': data}))
    return JSONResponse({'code': code, 'msg': msg, 'data': data}, status_code=status_code)
    # return {'code': code, 'msg': msg, 'data': data}


def check_token(jwt):
    return User(jwt=jwt, user_id=1)


async def verify_token(req: Request) -> User:
    jwt = req.headers.get('orange-jwt')
    if not jwt:
        jwt = req.headers.get('orange-jwt')
    if not jwt:
        raise CustomError('no jwt')
    try:
        return check_token(jwt)
    except Exception as e:
        logger.error('jwt error:{} jwt: {}'.format(e, jwt))
        raise CustomError('jwt error:{},jwt: {}'.format(e, jwt))


from sqlalchemy.orm import sessionmaker, scoped_session


# async def get_db(auto_migrations=False):
#     if not G.DBSession:
#         G.DBSession = new_session_factory(Config.db_url, auto_migrations=auto_migrations,
#                                           pool_recycle=Config.db_pool_recycle)
#     if not G.db:
#         G.db = G.DBSession()
#
#     try:
#         # 查看session是否还能用
#         G.db.execute('select 1')
#     except:
#         G.db.close()  # 扔回连接池
#         G.db = G.DBSession()
#
#     G.db.expire_all()
#     return G.db


async def get_rds():
    if G.rds:
        return G.rds
    try:
        redis_store = redis.StrictRedis(host=Config.rds_host, port=Config.rds_port,
                                        password=Config.rds_password, db=Config.rds_db,
                                        decode_responses=True)
        G.rds = redis_store
        return redis_store
    except Exception as e:
        raise CustomError('connect redis error:{}'.format(e))


class OrDepends:
    # @classmethod
    # def db(cls):
    #     return Depends(get_db)

    @classmethod
    def rds(cls):
        return Depends(get_rds)

    @classmethod
    def verify_token(cls):
        return Depends(verify_token)
