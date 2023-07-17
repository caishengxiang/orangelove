# ---encoding:utf-8---
# @Time    : 2023/7/16 23:02
# @Author  : caishengxiang
# @Email   : 383301857@qq.com
# @File    : orm.py
# @Project : orangelove
import json
import asyncio
from datetime import datetime
from sqlalchemy import JSON,Column
from sqlalchemy import INTEGER, VARCHAR,ARRAY,BOOLEAN,TIMESTAMP
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """
    用户表
    us: user的缩写
    """
    __tablename__ = 'us_user'

    user_id = Column(INTEGER, primary_key=True, comment='用户ID', autoincrement=True, nullable=False,
                     unique=True)  # autoincrement 自增
    # 用户名(一般是手机)            # 不能为空,唯一约束,索引  在PostgreSQL中空值(NULL)与空串(‘’)并非等同,且NULL不影响unique约束
    username = Column(VARCHAR(40), nullable=False, unique=True, index=True, comment='用户名')
    # 密码，MD5后的值
    password = Column(VARCHAR(255), nullable=False, comment='hash密码')
    # token(用户登陆成功后令牌)
    token = Column(VARCHAR(255), server_default='', comment='token')
    # 个性签名
    signature = Column(VARCHAR(255), server_default='', comment='个性签名')
    # 头像图片路径
    avatar_url = Column(VARCHAR(128), server_default='', comment='头像图片路径')
    # 姓名
    nick_name = Column(VARCHAR(255), index=True, comment='姓名')
    # 手机
    phone = Column(INTEGER, unique=True, index=True, comment='手机')
    # 邮箱
    email = Column(VARCHAR(80), unique=True, index=True, comment='邮箱')
    # 角色id
    role_ids = Column(ARRAY(INTEGER), server_default='{1}', comment='用户角色id')
    # 是否超级管理员
    is_admin = Column(BOOLEAN, server_default='False', comment='是否管理员')
    # 逻辑删除
    is_deleted = Column(BOOLEAN, server_default='False', comment='逻辑删除')
    # 创建时间
    create_time = Column(TIMESTAMP, default=func.now(), comment='创建时间')
    # 修改时间
    update_time = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), comment='修改时间')

    def get_permissions_list(self):
        """因sqlalchemy内部原因,函数不能命名为 permissions/get_permissions"""
        permission_codes = []
        for role_id in self.role_ids:
            role = g.db.query(Role).filter(Role.role_id == role_id).first()
            permission_codes.extend(getattr(role, 'permission_codes', []))
        return permission_codes

    # @classmethod
    # def set_user_info(cls, user_model=None, user_id=None, token=None):
    #     """设置redis用户信息缓存缓存"""
    #     if user_model is None:
    #         filter_params = [~User.is_deleted]
    #         if user_id:
    #             filter_params.append(User.user_id == user_id)
    #         elif token:
    #             filter_params.append(User.token == token)
    #         user_model = g.db.query(cls).filter(*filter_params).first()
    #
    #     if not user_model:
    #         raise BizError('用户已在别处登陆,请重新登陆', code=ERROR.Unauthorized)
    #
    #     user_info = user_model.to_dict()
    #     user_info['permission_codes'] = user_model.get_permissions_list()
    #
    #     # 更新缓存
    #     user_json = json.dumps(user_info)  # 必须是flask自带的json,标准库的json 不识别datatime类型
    #     token_key = RedisKey.token(token)
    #     g.rds.setex(token_key, RedisKey.TOKEN_TIME, user_json)  # 缓存 token:user_info
    #     return user_info


class Role(CustomModel):
    """ 角色
    """
    __tablename__ = 'us_role'
    role_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(30), unique=True, nullable=False, server_default='', comment='名称')
    # permission_names = Column(CustomList(3000), nullable=False, server_default='', comment='权限名称列表')  # mysql
    permission_codes = Column(ARRAY(String), nullable=False, server_default='{}', comment='权限名称列表')
    remark = Column(VARCHAR(3000), nullable=False, server_default='', comment='备注')


class Permission(CustomModel):
    """ 权限
    """
    __tablename__ = "us_permission"
    permission_code = Column(VARCHAR(30), primary_key=True, nullable=False, comment='权限code(英文名)')
    permission_name = Column(VARCHAR(30), nullable=False, unique=True, comment='权限名称')
    module_name = Column(VARCHAR(30), nullable=False, server_default='', comment='权限模块名称')
    module_code = Column(VARCHAR(30), nullable=False, server_default='', comment='权限模块code(英文名)')
    remark = Column(VARCHAR(3000), nullable=False, server_default='', comment='备注')
