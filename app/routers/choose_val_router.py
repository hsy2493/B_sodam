from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schema.ycw_schema import ChooseValCreate, ChooseValResponse
from app.services.ycw_service import Choose_val_service
from app.database.database import get_db
from typing import List

choose_router = APIRouter(
    prefix="/choose_val",
    tags=["choose_val"]
)

# 등록
@choose_router.post("", response_model=ChooseValResponse)
def add_choose(choose_val: ChooseValCreate, db: Session = Depends(get_db)):
    return Choose_val_service.create_choose_val(db=db, choose_val=choose_val)

# 전체 조회
@choose_router.get("s", response_model=List[ChooseValResponse])
def read_chooses(db: Session = Depends(get_db)):
    return Choose_val_service.get_all_choose_vals(db)

# 단일 조회
@choose_router.get("/{choose_id}", response_model=ChooseValResponse)
def read_choose(choose_id: int, db: Session = Depends(get_db)):
    return Choose_val_service.get_choose_val_by_id(db, choose_id)

# 수정
@choose_router.put("/{choose_id}", response_model=ChooseValResponse)
def update_choose(choose_id: int, choose: ChooseValCreate, db: Session = Depends(get_db)):
    return Choose_val_service.update_choose_val(db, choose_id, choose)

# 삭제
@choose_router.delete("/{choose_id}")
def delete_choose(choose_id: int, db: Session = Depends(get_db)):
    return Choose_val_service.delete_choose_val(db, choose_id)