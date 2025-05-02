from sqlalchemy.orm import Session # SQLAlchemy 세션 관리
from app.models.sql_member import SQLMember # SQLAlchemy 모델
from app.schema.member import UpdateModel, UpdatePwd, FindPwd,  AdminUpdate # schema : DTO
from fastapi import HTTPException # 예외 처리

# 유효성 검사
# 로그인(이름, 닉네임, 전화번호, 아이디), 내정보 조회  
def get_member_by_email(db: Session, email: str): # 이메일로 회원정보 조회
    return db.query(SQLMember).filter(SQLMember.email == email).first() # db 조회

# 아이디 찾기(이름, 전화번호)
def get_member_by_name_and_phon_num(db: Session, name: str, phon_num: str): # 이름과 전화번호로 회원정보 조회
    return db.query(SQLMember).filter(SQLMember.name == name, SQLMember.phon_num == phon_num).first() # db 조회

# 아이디 찾기/비밀번호 찾기
# 아이디 찾기
def find_member_id(db: Session, name: str, phon_num: str): 
    db_member =  get_member_by_name_and_phon_num(db, name, phon_num) # db로 member 조회
    if db_member: # 이름과 전화번호로 member 조회 
        return db_member.email # 조회된 아이디 반환
    return None # 조회된 데이터가 없는 경우, 무효화(None) 반환
    
# 비밀번호 찾기 
def find_member_pwd(db: Session, email: str, temp_pwd: FindPwd): # 이메일과 비밀번호로 회원정보 조회
    db_member = get_member_by_email(db, email) # db로 member 조회
    if db_member: 
        db_member.pwd = temp_pwd # db에 이메일로 발송된 임시 비밀번호 업데이트
        db.commit() # db에 커밋
        db.refresh(db_member) # db에 반영
        return temp_pwd   # 발송 성공
    return None  # 발송 실패, None 반환


# 관리자 페이지
# 전체 회원정보 조회
def all_member(db: Session): # 전체 member 조회
    db_member = db.query(SQLMember).all()  # db 조회
    return db_member 

# 일부 회원정보 조회 (이름)
def get_admin_member_by_name(db: Session, member_name: str): # 이름으로 member 조회
    return db.query(SQLMember).filter(SQLMember.name == member_name).all() # db 조회

# 유효성 검사
# 로그인(이름, 닉네임, 전화번호, 아이디), 내정보 조회  
def get_admin_member_by_email(db: Session, member_email: str): # 이메일로 회원정보 조회
    return db.query(SQLMember).filter(SQLMember.email == member_email).first() # db 조회
        
# 회원정보 수정 (이메일, 이름, 닉네임, 전화번호)
def admin_update_member(db: Session, member_email: str, update_data : AdminUpdate): # 이메일로 내정보 업데이트 
    db_member = get_admin_member_by_email(db, member_email) # db로 member 조회 
    if db_member: # is not None : 값이 None인지 명확히 파악함. 
        if update_data.email is not None: # 이메일 : 값이 None인지 아닌지 파악
            db_member.email = update_data.email # None 아닌 경우, 업데이트
        if update_data.name is not None: # 이름
            db_member.name = update_data.name 
        if update_data.nickname is not None: # 닉네임 
            db_member.nickname = update_data.nickname
        if update_data.phon_num is not None: # 전화번호
            db_member.phon_num = update_data.phon_num
        db.commit() # 변경사항 db에 저장 
        db.refresh(db_member) # 최신 데이터 보장
        return db_member # 수정된 데이터 반환
    return None # 수정된 데이터가 없는 경우, None 반환(업데이트 실패)
            
# 회원탈퇴 (이메일)
""" 
def admin_delete_member(db: Session, member_email: str): # 이메일로 회원탈퇴 
    db_member = get_admin_member_by_email(db, member_email) # db로 member 조회 
    if db_member: 
        db.delete(db_member) # 이메일로 member 삭제
        db.commit()
        return db_member
    return None # 탈퇴회원 데이터 없는 경우, None 반환(탈퇴 실패) 
"""
            
# 마이페이지 
# 내정보 수정 (이메일, 닉네임, 전화번호)
def update_member(db: Session, email: str, update_data: UpdateModel): # 이메일로 내정보 업데이트
    db_member = get_member_by_email(db, email) # db로 member 조회 
    if db_member: 
        if update_data.email is not None: # 이메일 
            db_member.email = update_data.email  # db에 수정된 데이터 업데이트 
        if update_data.nickname is not None: # 닉네임 
            db_member.nickname = update_data.nickname
        if update_data.phon_num is not None: # 전화번호 
            db_member.phon_num = update_data.phon_num
        db.commit() # db에 커밋
        db.refresh(db_member) # db에 반영
        return db_member # 수정된 데이터 반환 
    return None # 수정된 데이터가 없는 경우, None 반환

# 비밀번호 변경
def update_member_password(db: Session, email: str, update_pwd: UpdatePwd): # 이메일로 비밀번호 업데이트
    db_member = get_member_by_email(db, email)  # db로 member 조회 
    if db_member: 
        if db_member.pwd == update_pwd.pwd: # 현재 비밀번호 확인
            if update_pwd.new_pwd: # 새 비밀번호 확인 
                db_member.pwd = update_pwd.new_pwd # db에 수정된 데이터 업데이트
                db.commit() # db에 커밋
                db.refresh(db_member) # db에 반영
                return db_member # 수정된 데이터 반환
            else: # 기존 비밀번호와 새 비밀번호 텍스트가 같은 내용인 경우
                raise HTTPException(status_code=400, detail="새 비밀번호를 입력해주세요.")
        else: # 일치하지 않은 경우 
            raise HTTPException(status_code=400, detail="현재 비밀번호가 일치하지 않습니다.")
    return None # 수정된 데이터가 없는 경우, None 반환
