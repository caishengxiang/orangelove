# ---encoding:utf-8---
# @Time    : 2023/7/13 00:51
# @Author  : caishengxiang
# @Email   : 383301857@qq.com
# @File    : log.py
# @Project : orangelove

# -*-coding:utf-8-*-
import os
import logging
import pathlib
from logging.handlers import TimedRotatingFileHandler
import logging.config
from orangelove.common.config import Config

if not os.path.exists(Config.LOG_DIR):
    pathlib.Path(Config.LOG_DIR).mkdir(parents=True, exist_ok=True)  # 创建目录

level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}


def get_logger():
    logger = logging.getLogger('ORANGE')  # log文件名
    logger.disabled = False  # 等同 fileConfig() 的 disable_existing_loggers=False
    format_str = logging.Formatter('%(asctime)s - %(pathname)s - [line:%(lineno)d] - %(levelname)s > %(message)s')
    logger.setLevel(level_relations.get(Config.LOGGER_LEVEL))
    sh = logging.StreamHandler()
    sh.setFormatter(format_str)
    logger.addHandler(sh)

    sh2 = TimedRotatingFileHandler(os.path.join(Config.LOG_DIR, 'service.log'), 'midnight', 1, 90, 'utf-8', True)
    sh2.setFormatter(format_str)
    logger.addHandler(sh2)
    logger.propagate = 0
    return logger


def get_error_logger():
    error_logger = logging.getLogger('ORANGE_ERROR')  # log文件名
    error_logger.disabled = False  # 等同 fileConfig() 的 disable_existing_loggers=False
    format_str = logging.Formatter('%(asctime)s - %(pathname)s - [line:%(lineno)d] - %(levelname)s > %(message)s')
    error_logger.setLevel(level_relations.get(Config.LOGGER_LEVEL))
    sh = logging.StreamHandler()
    sh.setFormatter(format_str)
    error_logger.addHandler(sh)

    sh2 = TimedRotatingFileHandler(os.path.join(Config.LOG_DIR, 'error.log'), 'midnight', 1, 90, 'utf-8', True)
    sh2.setFormatter(format_str)
    error_logger.addHandler(sh2)
    error_logger.propagate = 0
    return error_logger


logger = get_logger()
error_logger = get_error_logger()

logging.getLogger("kubernetes").setLevel(logging.INFO)  # 兼容k8s

if __name__ == '__main__':
    print(Config.LOG_DIR)
    logger.info('info')
    logger.debug('debug')
    logger.warning('警告')
    logger.error('报错')
    logger.critical('严重')
    error_logger.info('error info')