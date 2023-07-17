# ---encoding:utf-8---
# @Time    : 2023/7/16 23:04
# @Author  : caishengxiang
# @Email   : 383301857@qq.com
# @File    : db_tools.py
# @Project : orangelove
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool, StaticPool
from sqlalchemy import delete, select, update

async def async_main() -> None:
    engine = create_async_engine(
        "postgresql+asyncpg://scott:tiger@localhost/test",
        echo=True,
    )