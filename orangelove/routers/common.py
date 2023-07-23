# -*-coding:utf-8-*-
# -*-coding:utf-8-*-
import asyncio
import json
import time
import anyio

from fastapi import APIRouter, Request, BackgroundTasks, Depends, Query
from orangelove.common.errors import CustomError
from fastapi import params
from pydantic import BaseModel
from typing import Union
from orangelove.common.utils.fastapi_tools import OrDepends, render

common_router = APIRouter(
    prefix="/common",
    tags=["common"],
    responses={404: {"description": "Not found"}},
)


@common_router.api_route(path="/healthy", methods=['GET', "POST"])
async def healthy():
    return render()
