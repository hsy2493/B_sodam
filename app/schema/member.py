# app/schema/member.py
from pydantic import BaseModel
from datetime import datetime

# MemberDTO
class MemberBase(BaseModel): # member 테이블 베이스 모델 
    email: str # 이메일(아이디)
    name: str # 이름
    nickname: str # 닉네임
    pwd: str # 비밀번호(password)
    phon_num: str  # 전화번호
    reg_date: datetime # 생성일 (기본값 : 현재 시각)
    upt_date: datetime  # 수정일 (기본값 : 현재 시각)
    class Config: # 일부 유저 조회
        orm_mode = True
        
# 로그인 유효성 검사 
class LoginModel(BaseModel): # 로그인 모델
    email: str
    pwd: str
    class Config: 
        orm_mode = True

# 관리자 페이지 
class AdminUpdate(BaseModel): # 회원정보 수정 모델 (선택적) 
    email : str | None = None # 이메일(아이디)
    name: str | None = None # 이름 
    nickname : str | None = None # 닉네임 
    phon_num : str | None = None # 전화번호  
    class Config: 
        orm_mode = True
    
# 마이페이지     
class MypageModel(BaseModel): # 마이페이지 조회 모델
    email: str # 이메일(아이디)
    name: str # 이름
    nickname: str # 닉네임
    phon_num: str # 전화번호
    class Config: 
        orm_mode = True

class UpdateModel(BaseModel): # 마이페이지 수정 모델 (선택적)
    email: str | None = None # 이메일(아이디)
    nickname: str | None = None # 닉네임
    phon_num: str | None = None # 전화번호
    class Config: 
        orm_mode = True

class UpdatePwd(BaseModel): # 비밀번호 변경 모델
    email : str # 이메일(아이디) 
    new_pwd : str | None = None # 새 비밀번호
    pwd : str | None = None # 비밀번호 
    class Config: 
        orm_mode = True

class MemberCreate(BaseModel): # 회원가입
    email: str
    name: str
    nickname: str
    pwd: str
    phon_num: str
    class Config:
        orm_mode = True

# 아이디 찾기/비밀번호 찾기
class FindID(BaseModel): # 아이디 찾기 모델
    name: str # 이름
    phon_num: str # 전화번호
    class Config: 
        orm_mode = True
    
class FindPwd(BaseModel): # 비밀번호 찾기 모델
    email: str # 이메일(아이디)
    class Config: 
        orm_mode = True


class Member(MemberBase): # member 테이블의 전체 스키마(MemberBase) 데이터 지정
    class Config: # Pydantic 모델 설정
        from_attributes = True # SQLAlchemy 모델(SQLMember)과 호환
        orm_mode = True
        
