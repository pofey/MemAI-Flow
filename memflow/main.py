"""
程序启动入口类
"""
import os

from memflow.exceptions import CuboxErrorException

if not os.environ.get("WORKDIR"):
    workdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app/memflow')
    if not os.path.exists(workdir):
        os.makedirs(workdir)
        os.makedirs(os.path.join(workdir, 'logs'))
    os.environ["WORKDIR"] = workdir
import logging.config
import inject

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.exceptions import RequestValidationError

from memflow.common.logging import LOGGING_CONFIG
from memflow.memapi import MemApi

logging.config.dictConfig(LOGGING_CONFIG)

import httpx
import uvicorn
from starlette.exceptions import HTTPException
from fastapi import FastAPI
from memflow.databases import create_all

from memflow.common.response import json_200, json_500, json_with_status
from memflow.models import *

scheduler = BackgroundScheduler(daemon=True)

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
        message='Parameter error',
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
    api_key = os.environ.get("MEM_API_KEY")
    if not api_key:
        raise CuboxErrorException("MEM_API_KEY not found, please set it in env")
    mem = MemApi(api_key)
    binder.bind(MemApi, mem)


def startup():
    inject.configure(config)
    from memflow.tasks.cuboxsynctask import CuboxSyncTask
    auth_code = os.environ.get("CUBOX_AUTH_CODE")
    if not auth_code:
        raise CuboxErrorException("CUBOX_AUTH_CODE not found, please set it in env")
    interval_secs = os.environ.get('CUBOX_SYNC_INTERVAL', 300)
    scheduler.add_job(CuboxSyncTask(auth_code).run, 'interval',
                      seconds=interval_secs)
    log.info("add job cubox sync task, interval: %s seconds" % interval_secs)
    scheduler.start()


if __name__ == "__main__":
    startup()
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("WEB_PORT", 8000))
