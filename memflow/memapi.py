import httpx
from tenacity import retry, wait_random_exponential, stop_after_attempt

CREATE_MEM_API = "https://api.mem.ai/v0/mems"


class MemApi:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": "ApiAccessToken " + self.api_key,
        }

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    def create_mem(self, content: str):
        params = {
            "content": content
        }
        r = httpx.post(CREATE_MEM_API, json=params, headers=self.headers)
        r.raise_for_status()
        return r.json()
