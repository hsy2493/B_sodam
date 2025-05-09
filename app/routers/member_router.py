from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request  # 라우터 처리, 예외 처리, 의존성 주입
from sqlalchemy.orm import Session  # SQLAlchemy 세션
from app.database.database import get_db  # DB 연결
from app.services import member_service  # member service
from app.schema.member import LoginModel, MemberBase, MypageModel, UpdateModel, UpdatePwd, FindID, FindPwd, AdminUpdate  # DTO

router = APIRouter(
    prefix="/login",  # 클래스 공통 경로
    tags=["member"]  # 제목
)


# 로그인 유효성 검사
@router.post("/member", response_model=MemberBase)
def login(request: Request, data: LoginModel, db: Session = Depends(get_db)):
    # memeber 아이디와 비밀번호 조회
    user = member_service.get_member_by_email(db, data.email)

    # 입력값과 db 데이터 유효성 검사
    if not user or not member_service.verify_password(data.pwd, user.pwd):  # 로그인 실패: 비밀번호 검증
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 올바르지 않습니다.")

    # 이메일 세션 처리
    request.session["user_email"] = user.email

    # 응답 데이터 반환
    return MemberBase(  # 응답 데이터
        email=user.email,
        name=user.name,
        nickname=user.nickname,
        pwd=user.pwd,
        phon_num=user.phon_num,
        reg_date=user.reg_date,
        upt_date=user.upt_date,
    )


# 로그아웃
@router.post("/logout")
def logout(request: Request):
    request.session.clear()  # 세션 무효화(삭제)
    return {"msg": "로그아웃 성공!"}


# 아이디 찾기
@router.post("/findid")
def find_id(data: FindID, db: Session = Depends(get_db)):
    user_id = member_service.find_member_id(db, data.name, data.phon_num)  # 이름과 이메일로 member 아이디 조회
    if user_id:  # 존재하는 경우
        return {"email": user_id}
    else:  # 존재하지 않은 경우
        raise HTTPException(status_code=404, detail="존재하지 않는 회원입니다.")  # 예외 처리


# 비밀번호 찾기
@router.post("/findpwd")
def find_pwd(data: FindPwd, db: Session = Depends(get_db)):
    # member 정보 조회
    user = member_service.get_member_by_email(db, data.email)  # 이메일로 member 조회
    if not user:  # 존재하지 않는 경우
        raise HTTPException(status_code=404, detail="존재하지 않는 회원입니다.")  # 예외 처리

    # 임시 비밀번호 생성 및 발송
    temp_pwd_plain = member_service.generate_and_update_temp_password(db, data.email)
    if temp_pwd_plain:  # 발송 성공
        return {"temp_pwd": temp_pwd_plain}  # 임시 비밀번호
    else:  # 발송 실패
        raise HTTPException(status_code=500, detail="임시 비밀번호 발송에 실패하였습니다.")  # 예외 처리


# 관리자 페이지
# 전체 회원정보 조회
@router.get("/admin")
def admin_all_member(db: Session = Depends(get_db)):  # 전체 member 조회
    all_member = member_service.get_all_members(db)  # db 조회
    return all_member  # 전체 회원 조회


# 일부 회원정보 조회(이름)
@router.get("/admin/{member_name}", response_model=List[MemberBase])
def admin_member_name(member_name: str, db: Session = Depends(get_db)):
    member = member_service.get_admin_member_by_name(db, member_name)  # 이름으로 member 조회
    if not member:
        raise HTTPException(status_code=404, detail="존재하지 않는 회원입니다.")  # 예외 처리
    return member


# 회원정보 수정
@router.put("/admin/{member_email}", response_model=MemberBase)  # 일부만 수정
def admin_update_member(member_email: str, data: AdminUpdate, db: Session = Depends(get_db)):
    update_member = member_service.admin_update_member(db, member_email, data)
    if not update_member:
        raise HTTPException(status_code=404, detail="존재하지 않는 회원입니다.")  # 예외 처리
    return update_member


# 마이페이지
# 내정보 조회
@router.get("/mypage/{email}", response_model=MypageModel)
def read_mypage(email: str, request: Request, db: Session = Depends(get_db)):
    # 이메일 세션 처리
    user_email = request.session.get("user_email")
    # 세션 유지x
    if not user_email or user_email != email:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    # member 정보 조회
    user = member_service.get_member_by_email(db, email)  # 이메일로 member 조회
    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 회원입니다.")  # 예외 처리

    # 응답 데이터 반환
    return MypageModel(  # 응답 데이터
        email=user.email,
        name=user.name,
        nickname=user.nickname,
        phon_num=user.phon_num
    )


# 내정보 수정
@router.put("/mypage/{email}", response_model=MypageModel)  # 일부만 수정
def update_mypage(email: str, data: UpdateModel, db: Session = Depends(get_db)):
    # member 정보 조회
    user = member_service.get_member_by_email(db, email)  # 이메일로 member 조회
    if not user:  # 예외 처리
        raise HTTPException(status_code=404, detail="존재하지 않는 회원입니다.")

    # 이메일 중복 검사
    if data.email:
        exist_user = member_service.get_member_by_email(db, data.email)  # 유효성 검사
        if exist_user and exist_user.email != email:  # 예외 처리
            raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")

    updated_user = member_service.update_member(db, email, data)
    if updated_user:
        # 응답 데이터
        return MypageModel(  # 수정 데이터 MypageModel에 반환
            email=updated_user.email,
            name=updated_user.name,
            nickname=updated_user.nickname,
            phon_num=updated_user.phon_num,
        )

    raise HTTPException(status_code=500, detail="내정보 수정 실패")  # 예외 처리


# 비밀번호 변경
@router.put("/mypage/{email}/pwd", response_model=MypageModel)  # 비밀번호만 변경
def update_pwd(email: str, data: UpdatePwd, db: Session = Depends(get_db)):
    # member 정보 조회
    user = member_service.get_member_by_email(db, email)  # 이메일로 member 조회
    if not user:  # 예외 처리
        raise HTTPException(status_code=404, detail="존재하지 않는 회원입니다.")

    # 새 비밀번호 업데이트 (해싱은 서비스 레이어에서)
    updated_user = member_service.update_member_password(db, email, data)
    if updated_user:
        # 응답 데이터
        return MypageModel(
            email=updated_user.email,
            name=updated_user.name,
            nickname=updated_user.nickname,
            phon_num=updated_user.phon_num,
        )

    raise HTTPException(status_code=400, detail="비밀번호 변경 실패")  # 예외 처리