from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship # 테이블간 관계 정의시 사용
from app.database.database import Base
from datetime import datetime

# 선택값 테이블 모델
class Choose_val_Model(Base):
    __tablename__ = "choose_val"
    choose_id = Column(Integer, primary_key=True, index=True)
    chat_log_id = Column(String(20)) # , ForeignKey('chat_log.chat_log_id')
    high_loc = Column(String(100))
    low_loc = Column(String(100))
    theme1 = Column(String(100))
    theme2 = Column(String(100))
    theme3 = Column(String(100))
    theme4 = Column(String(100))
    days = Column(Integer)
    regdate = Column(DateTime, default=datetime.now)
    uptdate = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 관계: 하나의 대화 → 하나의 선택값들
    # chat_log = relationship("ChatLog", back_populates="choose_val")

# 지역리스트 테이블 모델
class Area_list_Model(Base):
    __tablename__ = "area_list"
    area_list_id = Column(Integer, primary_key=True, index=True)
    chat_log_id = Column(String(20)) # , ForeignKey('chat_log.chat_log_id')
    title = Column(String(100))
    mapx = Column(String(100))
    mapy = Column(String(100))
    contenttypeid = Column(String(100))
    firstimage = Column(String(100))
    firstimage2 = Column(String(100))
    tel = Column(String(100))
    addr1 = Column(String(100))
    addr2 = Column(String(100))
    regdate = Column(DateTime, default=datetime.now)
    uptdate = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 관계: 하나의 대화 → 여러 추천지역
    # chat_log = relationship("ChatLog", back_populates="area_list")