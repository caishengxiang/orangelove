# ---encoding:utf-8---
# @Time    : 2023/7/12 23:31
# @Author  : caishengxiang
# @Email   : 383301857@qq.com
# @File    : config.py
# @Project : orangelove
import os
import json

env = os.environ
ENV = env.get('OR_ENV', 'DEV')


class BaseConfig:
    db_username = env.get('OR_DB_URL_USERNAME', 'root')
    db_password = env.get('OR_DB_PSW', 'Admin_123')
    db_name = env.get('OR_DB_NAME', 'orangelove')
    db_host = env.get('OR_DB_HOST', 'localhost')
    db_port = env.get('OR_DB_PORT', '5432')
    db_pool_recycle = int(env.get('OR_POOL_RECYCLE', 1800))  # 数据库连接回收时间

    LOG_DIR = os.getenv('LOG_DIR', '/tmp/orange_logs')
    LOGGER_LEVEL = env.get('LOGGER_LEVEL', 'info')


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DEBUG = False


class ProduceConfig(BaseConfig):
    DEBUG = False


Config = {
    "DEV": DevConfig(),
    "TEST": TestConfig(),
    "PRODUCE": ProduceConfig()
}.get(ENV.upper())
