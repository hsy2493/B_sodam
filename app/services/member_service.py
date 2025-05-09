from sqlalchemy.orm import Session
from app.models.sql_member import SQLMember
from app.schema.member import UpdateModel, UpdatePwd, AdminUpdate
from fastapi import HTTPException
from passlib.hash import bcrypt # 비밀번호 해싱 
from app.schema.randompwd import RandomPwd  # 랜덤 비밀번호 


# 유효성 검사
def get_member_by_email(db: Session, email: str):  # 이메일로 회원정보 조회
    return db.query(SQLMember).filter(SQLMember.email == email).first()  # db 조회

def get_member_by_name_and_phon_num(db: Session, name: str, phon_num: str):  # 이름과 전화번호로 회원정보 조회
    return db.query(SQLMember).filter(SQLMember.name == name, SQLMember.phon_num == phon_num).first()  # db 조회


# 아이디 찾기
def find_member_id(db: Session, name: str, phon_num: str):
    db_member = get_member_by_name_and_phon_num(db, name, phon_num)  # db로 member 조회
    if db_member:  # 이름과 전화번호로 member 조회
        return db_member.email  # 조회된 아이디 반환
    return None  # 조회된 데이터가 없는 경우, 무효화(None) 반환


# 비밀번호 해싱 및 검증 
# 비밀번호 검증 함수 (Spring Security BCryptPasswordEncoder와 호환)
def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)

# 비밀번호 해싱 함수 (Spring Security BCryptPasswordEncoder와 호환)
def get_password_hash(password):
    return bcrypt.hash(password)

# 비밀번호 찾기 - 임시 비밀번호 생성 및 업데이트 (해싱된 값 저장)
def update_member_password_by_email(db: Session, email: str, new_password_plain: str):
    db_member = get_member_by_email(db, email)  # db로 member 조회
    if db_member:
        hashed_temp_pwd = get_password_hash(new_password_plain)
        db_member.pwd = hashed_temp_pwd  # db에 이메일로 발송된 임시 비밀번호 업데이트 (해싱하여 저장)
        db.commit()  # db에 커밋
        db.refresh(db_member)  # db에 반영
        return True
    return False


# 비밀번호 찾기 - 임시 비밀번호 생성 및 반환 (라우터에서 호출)
def generate_and_update_temp_password(db: Session, email: str):
    db_member = get_member_by_email(db, email)
    if db_member:
        random_pwd_generator = RandomPwd()  # RandomPwd 객체 생성
        temp_pwd_plain = random_pwd_generator.random_password(length=20)
        hashed_temp_pwd = get_password_hash(temp_pwd_plain)
        db_member.pwd = hashed_temp_pwd
        db.commit()
        db.refresh(db_member)
        return temp_pwd_plain
    return None


# 관리자 페이지
# 전체 회원정보 조회
def get_all_members(db: Session):  # 전체 member 조회
    db_member = db.query(SQLMember).all()  # db 조회
    return db_member


# 일부 회원정보 조회 (이름)
def get_admin_member_by_name(db: Session, member_name: str):  # 이름으로 member 조회
    return db.query(SQLMember).filter(SQLMember.name == member_name).all()  # db 조회


# 회원정보 수정 (이메일, 이름, 닉네임, 전화번호)
def admin_update_member(db: Session, member_email: str, update_data: AdminUpdate):  # 이메일로 내정보 업데이트
    db_member = get_member_by_email(db, member_email)  # db로 member 조회
    if db_member:  # is not None : 값이 None인지 명확히 파악함.
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(db_member, field, value)  # None 아닌 경우, 업데이트
        db.commit()  # 변경사항 db에 저장
        db.refresh(db_member)  # 최신 데이터 보장
        return db_member  # 수정된 데이터 반환
    return None  # 수정된 데이터가 없는 경우, None 반환(업데이트 실패)


# 마이페이지
# 내정보 수정 (이메일, 닉네임, 전화번호)
def update_member(db: Session, email: str, update_data: UpdateModel):  # 이메일로 내정보 업데이트
    db_member = get_member_by_email(db, email)  # db로 member 조회
    if db_member:
        for field, value in update_data.dict(exclude_unset=True).items():
            if field == "email":
                existing_member = get_member_by_email(db, value)  # 유효성 검사
                if existing_member and existing_member.email != email:  # 예외 처리
                    raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")
            setattr(db_member, field, value)  # db에 수정된 데이터 업데이트
        db.commit()  # db에 커밋
        db.refresh(db_member)  # db에 반영
        return db_member  # 수정된 데이터 반환
    return None  # 수정된 데이터가 없는 경우, None 반환


# 비밀번호 변경 (새 비밀번호 해싱하여 저장)
def update_member_password(db: Session, email: str, new_password: UpdatePwd):  # 이메일로 비밀번호 업데이트
    db_member = get_member_by_email(db, email)  # db로 member 조회
    if db_member:
        hashed_new_pwd = get_password_hash(new_password.new_pwd)
        db_member.pwd = hashed_new_pwd  # db에 수정된 데이터 업데이트 (해싱)
        db.commit()  # db에 커밋
        db.refresh(db_member)  # db에 반영
        return db_member  # 수정된 데이터 반환
    return None  # 수정된 데이터가 없는 경우, None 반환