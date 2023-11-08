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
