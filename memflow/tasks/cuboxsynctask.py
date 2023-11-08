import logging
import time

import httpx
import inject
from tenacity import wait_random_exponential, retry, stop_after_attempt

from memflow.exceptions import CuboxErrorException
from memflow.memapi import MemApi
from memflow.models import SyncRecord
from trafilatura import extract

CHANNEL_NAME = "cubox"
INBOX_URL = "https://cubox.pro/c/api/v2/search_engine/inbox"
DETAIL_URL = "https://cubox.pro/c/api/v2/bookmark/detail"
_LOGGER = logging.getLogger(__name__)


def extract_data_from_response(response):
    if response.get("code") != 200:
        raise CuboxErrorException(
            "Response error,code: %s message: %s" % (response.get("code"), response.get("message")))
    return response.get("data")


class CuboxSyncTask:
    def __init__(self, authorization: str):
        self.authorization = authorization

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    def list_inbox(self, page: int = 1, asc: bool = False, archiving: bool = False):
        params = {
            "page": page,
            "asc": asc,
            "archiving": archiving,
        }
        headers = {
            "authorization": self.authorization,
            "referer": "https://cubox.pro/my/inbox"
        }
        r = httpx.get(INBOX_URL, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_detail(self, bookmark_id: int):
        params = {
            "bookmarkId": bookmark_id
        }
        headers = {
            "authorization": self.authorization,
            "referer": "https://cubox.pro/my/card"
        }
        r = httpx.get(DETAIL_URL, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

    def run(self):
        _LOGGER.info("start sync cubox content")
        data = extract_data_from_response(self.list_inbox())
        mem_api: MemApi = inject.instance(MemApi)
        for item in data:
            bookmark_id = item.get('userSearchEngineID')
            if SyncRecord.exists(CHANNEL_NAME, bookmark_id):
                continue
            time.sleep(1)
            _LOGGER.info(f"start sync cubox bookmark id: {bookmark_id}")
            detail = extract_data_from_response(self.get_detail(bookmark_id))
            page_content = extract(f"<html>{detail.get('content')}</html>", include_links=True,
                                   include_formatting=True,
                                   include_images=True)
            url = detail.get('targetURL')
            title = detail.get('title')
            markdown_content = f'## {title}\n\n[🔗原文链接]({url})\n\n{page_content}'
            r = mem_api.create_mem(markdown_content)
            mem_url = r.get('url')
            SyncRecord.insert(CHANNEL_NAME, bookmark_id, r.get('id'), mem_url)
            _LOGGER.info(f"create mem success, title: {title} mem_url: {mem_url}")
