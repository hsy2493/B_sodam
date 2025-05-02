# app/schema/qna_schema.py
from pydantic import BaseModel
from typing import Optional

class QnaCreate(BaseModel):
    """QNA 생성 스키마"""
    chat_log_id: str
    qna_id: str
    question: str
    answer: str
    reg_date: str
    upt_date: str

class QnaResponse(BaseModel):
    """QNA 응답 스키마"""
    question: str
    answer: str
     # commit추가