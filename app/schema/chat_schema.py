# app/schema/chat_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class ChatLogCreate(BaseModel):
    """채팅 로그 생성 스키마"""
    mem_email: EmailStr
    chat_log_id: str
    title: str
    reg_date: str
    upt_date: str

class ChatLogUpdate(BaseModel):
    """채팅 로그 업데이트 스키마"""
    chat_log_id: str
    title: str

class ChatLogResponse(BaseModel):
    """채팅 로그 응답 스키마"""
    reg_date: str
    title: str
     # commit추가