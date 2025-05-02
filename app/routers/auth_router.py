from fastapi import APIRouter, HTTPException, Depends, Query# 라우터 처리, 예외 처리, 의존성 주입
from sqlalchemy.orm import Session # SQLAlchemy 세션
from app.database.database import get_db # DB 연결
from app.models.sql_member import SQLMember # SQLAlchemy 모델
from sqlalchemy.exc import SQLAlchemyError
#from app.services.member_service import get_all_members # 유저 정보 조회
from app.schema.member import MemberCreate,Member # DTO
from datetime import datetime # reg_date, upt_date를 위해서 import

router = APIRouter(prefix="/auth", tags=["auth"])
#회원가입
@router.post("/register", response_model=Member)
async def register_user(user: MemberCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(SQLMember).filter(SQLMember.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
        db_nickname = db.query(SQLMember).filter(SQLMember.nickname == user.nickname).first()
        if db_nickname:
            raise HTTPException(status_code=400, detail="이미 존재하는 닉네임입니다.")

        # 1. SQLMember 모델 인스턴스 생성 및 데이터 할당
        db_member = SQLMember(
            email=user.email,
            name=user.name,
            nickname=user.nickname,
            pwd=user.pwd,
            phon_num=user.phon_num,
            reg_date=datetime.now(), # 현재 시각으로 설정
            upt_date=datetime.now()  # 현재 시각으로 설정
        )

        # 2. 세션에 추가
        db.add(db_member)
        # 3. 변경 사항 커밋 (데이터베이스에 저장)
        db.commit()
        # 4. 세션 갱신 (저장된 데이터 반영, 특히 id 값)
        db.refresh(db_member)

        return Member.from_orm(db_member) # 직접 Pydantic 객체로 변환해서 리턴
    except SQLAlchemyError as e:
        db.rollback()  # 실패 시 rollback 필수!
        raise HTTPException(status_code=500, detail=f"등록 중 오류 발생: {str(e)}")
# ✅ 이메일 중복 확인
@router.get("/check-email", response_model=Member)
async def check_email(email: str = Query(..., regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
                      db: Session = Depends(get_db)):
    # print("받은 이메일", email)
    user = db.query(SQLMember).filter(SQLMember.email == email).first()
    # print("sql 알케미 작동 ", user)
    if not user:
        raise HTTPException(status_code=400, detail="해당 이메일로 조회된 회원이 없습니다.")
    return Member.from_orm(user)

# ✅ 닉네임 중복 확인
@router.get("/check-nickname", response_model=Member)
async def check_nickname(nickname: str = Query(..., min_length=2, max_length=20), db: Session = Depends(get_db)):
    print("받은 닉네임", nickname)
    user = db.query(SQLMember).filter(SQLMember.nickname == nickname).first()
    print("sql 알케미 작동", user)
    if not user:
        raise HTTPException(status_code=400, detail="이미 존재하는 닉네임입니다.")
    return Member.from_orm(user)

