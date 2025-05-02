from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schema.ycw_schema import ChooseValCreate, AreaListCreate
from fastapi import HTTPException
from app.models.ycw_models import Choose_val_Model, Area_list_Model

# 선택값 CRUD 클래스
class Choose_val_service:
    # 생성
    def create_choose_val(db: Session, choose_val: ChooseValCreate):
        try:
            db_choose_val = Choose_val_Model(
                high_loc=choose_val.high_loc,
                low_loc=choose_val.low_loc,
                theme1=choose_val.theme1,
                theme2=choose_val.theme2,
                theme3=choose_val.theme3,
                theme4=choose_val.theme4,
                days=choose_val.days)
            db.add(db_choose_val)
            db.commit()
            db.refresh(db_choose_val)
            return db_choose_val
        except SQLAlchemyError as e:
            db.rollback()  # 실패 시 rollback 필수!
            raise HTTPException(status_code=500, detail=f"등록 중 오류 발생: {str(e)}")
        
    # 전체 조회
    def get_all_choose_vals(db: Session):
        return db.query(Choose_val_Model).all()

    # 단일 조회
    def get_choose_val_by_id(db: Session, choose_id: int):
        choose_val = db.query(Choose_val_Model).filter(Choose_val_Model.choose_id == choose_id).first()
        if choose_val is None:
            raise HTTPException(status_code=404, detail="Choose_val not found")
        return choose_val

    # 수정
    def update_choose_val(db: Session, choose_id: int, updated_data: ChooseValCreate):
        try:
            choose_val = db.query(Choose_val_Model).filter(Choose_val_Model.choose_id == choose_id).first()
            if choose_val is None:
                raise HTTPException(status_code=404, detail="Choose_val not found")

            choose_val.high_loc = updated_data.high_loc
            choose_val.low_loc = updated_data.low_loc
            choose_val.theme1 = updated_data.theme1
            choose_val.theme2 = updated_data.theme2
            choose_val.theme3 = updated_data.theme3
            choose_val.theme4 = updated_data.theme4
            choose_val.days = updated_data.days

            db.commit()
            db.refresh(choose_val)
            return choose_val
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"수정 중 오류 발생: {str(e)}")

    # 삭제
    def delete_choose_val(db: Session, choose_id: int):
        try:
            choose_val = db.query(Choose_val_Model).filter(Choose_val_Model.choose_id == choose_id).first()
            if choose_val is None:
                raise HTTPException(status_code=404, detail="Choose_val not found")

            db.delete(choose_val)
            db.commit()
            return {"message": f"Choose_val with id {choose_id} has been deleted"}
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"삭제 중 오류 발생: {str(e)}")

# 지역리스트 CRUD
class Area_list_service:
    # 생성 Area_list_Model AreaListCreate
    def create_area_list(db: Session, area_list: AreaListCreate):
        try:
            db_area_list = Area_list_Model(
                chat_log_id=area_list.chat_log_id,
                title=area_list.title,
                mapx=area_list.mapx,
                mapy=area_list.mapy,
                contenttypeid=area_list.contenttypeid,
                firstimage=area_list.firstimage,
                firstimage2=area_list.firstimage2,
                tel=area_list.tel,
                addr1=area_list.addr1,
                addr2=area_list.addr2)
            db.add(db_area_list)
            db.commit()
            db.refresh(db_area_list)
            return db_area_list
        except SQLAlchemyError as e:
            db.rollback()  # 실패 시 rollback 필수!
            raise HTTPException(status_code=500, detail=f"등록 중 오류 발생: {str(e)}")
        
    # 전체 조회
    def get_all_area_list(db: Session):
        return db.query(Area_list_Model).all()

    # 단일 조회
    def get_area_list_by_id(db: Session, area_list_id: int):
        area_list = db.query(Area_list_Model).filter(Area_list_Model.area_list_id == area_list_id).first()
        if area_list is None:
            raise HTTPException(status_code=404, detail="Area_list not found")
        return area_list

    # 수정
    def update_area_list(db: Session, area_list_id: int, updated_data: AreaListCreate):
        try:
            area_list = db.query(Area_list_Model).filter(Area_list_Model.area_list_id == area_list_id).first()
            if area_list is None:
                raise HTTPException(status_code=404, detail="Area_list not found")
            area_list.chat_log_id = updated_data.chat_log_id
            area_list.title = updated_data.title
            area_list.mapx = updated_data.mapx
            area_list.mapy = updated_data.mapy
            area_list.contenttypeid = updated_data.contenttypeid
            area_list.firstimage = updated_data.firstimage
            area_list.firstimage2 = updated_data.firstimage2
            area_list.tel = updated_data.tel
            area_list.addr1 = updated_data.addr1
            area_list.addr2 = updated_data.addr2

            db.commit()
            db.refresh(area_list)
            return area_list
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"수정 중 오류 발생: {str(e)}")

    # 삭제
    def delete_area_list(db: Session, area_list_id: int):
        try:
            area_list = db.query(Area_list_Model).filter(Area_list_Model.area_list_id == area_list_id).first()
            if area_list is None:
                raise HTTPException(status_code=404, detail="Choose_val not found")

            db.delete(area_list)
            db.commit()
            return {"message": f"Area_list with id {area_list_id} has been deleted"}
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"삭제 중 오류 발생: {str(e)}")