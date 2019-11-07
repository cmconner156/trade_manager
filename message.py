import datetime
from sqlalchemy import Column, Integer, DateTime, String, Float
from sqlalchemy_base import Base

class TGMessage(Base):
    __tablename__ = "tg_messages"
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    message_id = Column(String(15))
    sender_id = Column(String(15))
    received_date = Column(DateTime, default=datetime.datetime.utcnow)
    message_date = Column(DateTime, default=datetime.datetime.utcnow)
    channel_name = Column(String(255))
    channel_id = Column(String(15))
    raw_text = Column(String(255))
    status = Column(String(15))
    ack = Column(String(15), default = "FALSE")

