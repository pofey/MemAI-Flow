"""
程序启动入口类
"""
import json
import logging.config
import os

from fastapi.exceptions import RequestValidationError

from memflow.common.logging import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

import inject

import httpx
import uvicorn
from starlette.exceptions import HTTPException
from fastapi import FastAPI
from memflow.databases import create_all

from memflow.common.response import json_200, json_500, json_with_status
from memflow.models import *

log = logging.getLogger(__name__)

# 初始化ORM框架
create_all()

app = FastAPI()


# 加载所有fastapi的接口路由

@app.get("/")
async def root():
    """
    默认首页
    :return:
    """
    return json_200(message='memflow server')


@app.exception_handler(RequestValidationError)
async def unprocessable_entity_handler(request, exc: RequestValidationError):
    return json_with_status(
        status_code=422,
        message='参数错误',
        data=dict(exc.errors())
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return json_with_status(status_code=exc.status_code, message=exc.detail)


@app.exception_handler(httpx.HTTPStatusError)
async def http_status_exception_handler(request, e: httpx.HTTPStatusError):
    msg = e.response.json().get('error', {}).get('message')
    log.error('http status exception: ' + msg, exc_info=True)
    return json_500(message=msg)


@app.exception_handler(Exception)
async def universal_exception_handler(request, exc):
    log.error('universal_exception_handler', exc_info=True)
    return json_500(message=str(exc))


def config(binder):
    """
    依赖注入机制的初始化
    所有通过inject使用的对象，需要提前再此绑定
    :param binder:
    :return:
    """
    pass


if __name__ == "__main__":
    # 加载公共全局依赖
    inject.configure(config)
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("WEB_PORT", 8000))
