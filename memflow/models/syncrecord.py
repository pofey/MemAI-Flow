from typing import Optional, List

from memflow.databases import *


class SyncRecord(BaseDBModel):
    """
    存储站点用的一些Cookie
    """
    __tablename__ = 'cookie_store'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    channel = Column(String, comment='内容来源通道', nullable=False)
    content_id = Column(String, comment='内容的唯一编号，用于查询重复', nullable=False)
    mem_id = Column(String, comment='写入mem后的唯一编号', nullable=False)
    mem_url = Column(String, comment='写入mem后获得的访问链接', nullable=False)

    @staticmethod
    def exists(channel: str, content_id: str) -> bool:
        return SyncRecord.query().filter(
            (SyncRecord.channel == channel) & (SyncRecord.content_id == content_id)).first() is not None

    @staticmethod
    def insert(channel: str, content_id: str, mem_id: str, mem_url: str):
        record = SyncRecord()
        record.channel = channel
        record.content_id = content_id
        record.mem_id = mem_id
        record.mem_url = mem_url
        record.save()
