# app/models/sql_member.py
from sqlalchemy import Column, String, DateTime
from app.database.database import Base # db 정보

class SQLMember(Base):
    __tablename__ = "member" # member 테이블
    
    email = Column(String(100), primary_key=True)  # 이메일(아이디)
    name = Column(String(30), nullable=False) # 이름
    nickname = Column(String(60), nullable=False)  # 닉네임
    pwd = Column(String(200), nullable=False)  # 비밀번호(password)
    phon_num = Column(String(13), nullable=False)  # 전화번호 
    reg_date = Column(DateTime, nullable=False)  # 생성일
    upt_date = Column(DateTime, nullable=False)  # 수정일