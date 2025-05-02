from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 선택값 리퀘스트
class ChooseValCreate(BaseModel):
    high_loc: str
    chat_log_id: str
    low_loc: str
    theme1: str
    theme2: str
    theme3: Optional[str] = None
    theme4: Optional[str] = None
    days: int

# 선택값 리스폰스
class ChooseValResponse(ChooseValCreate):
    choose_id: int
    regdate: datetime
    uptdate: datetime

    class Config:
        orm_mode = True # SQLAlchemy로 생성된 데이터를 담을 수 있게 됨

# 지역리스트 리퀘스트
class AreaListCreate(BaseModel):
    chat_log_id: str
    title: str
    mapx: float
    mapy: float
    contenttypeid: str
    firstimage: Optional[str] = None
    firstimage2: Optional[str] = None
    tel: Optional[str] = None
    addr1: Optional[str] = None
    addr2: Optional[str] = None

# 지역리스트 리스폰스
class AreaListResponse(AreaListCreate):
    area_list_id: int
    regdate: datetime
    uptdate: datetime
    
    class Config:
        orm_mode = True