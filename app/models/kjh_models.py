# app/kjh_model.py
from sqlalchemy import Column, String, Date
from app.database.database import Base

class ChatLog(Base):
    __tablename__ = "chat_log"

    chat_log_id = Column(String(20), primary_key=True)  # e.g., a0001, a0002
    mem_email = Column(String(100), nullable=False)    # User email
    title = Column(String(100), nullable=False)        # Chat log title
    reg_date = Column(Date, nullable=False)            # Registration date
    upt_date = Column(Date, nullable=False)            # Update date

class Qna(Base):
    __tablename__ = "qna"
     # commit추가
    qna_id = Column(String(20), primary_key=True)      # e.g., b001, b002
    chat_log_id = Column(String(20), nullable=False)   # Foreign key to chat_log
    question = Column(String(500), nullable=False)     # User question
    answer = Column(String(2000), nullable=False)      # System answer
    reg_date = Column(Date, nullable=False)            # Registration date
    upt_date = Column(Date, nullable=False)            # Update date