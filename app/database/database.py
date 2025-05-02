import json # secrets.json = db 정보
import os 

from sqlalchemy import create_engine # 인코딩
from sqlalchemy.orm import sessionmaker # 세션 관리  
from sqlalchemy.ext.declarative import declarative_base # db 모델 정의 =  SQLAlchemy 모델 


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 디렉토리 경로 지정

SECRET_FILE = os.path.join(BASE_DIR, 'secrets.json') # db 관련 정보
secrets = json.loads(open(SECRET_FILE).read()) # db 정보 읽기 = json
db = secrets["DB"] # db키 정보 지정 

# secrets.json 정보 
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db.get('user')}:{db.get('password')}@{db.get('host')}:{db.get('port')}/{db.get('database')}?charset=utf8"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://<유저명>:<비밀번호>@<호스트>:<포트>/<DB이름>"?utf8 인코딩 

engine = create_engine( # 인코딩  
    SQLALCHEMY_DATABASE_URL,
    
    pool_size=5, # 데이터베이스 연결 풀의 기본 크기 (5명이 동시에 사용 가능)
    max_overflow=10, # 최대 초과 연결 수 (10명이 더 사용 가능)
    pool_timeout=30, # 연결 풀에서 대기 시간 (30초)
    pool_recycle=1800 # 연결 풀에서 재사용 가능한 최대 시간 (1800초 = 30분)

)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
# 세션 관리 = 세션 생성 (트랜잭션, 변경사항, 생성된 db 객체 관리)

Base = declarative_base() # db 베이스 클래스 :  SQLAlchemy 모델에 사용

def get_db(): # db 세션 관리 
    db = SessionLocal() # db 세션 생성 
    try:
        yield db # db 세션 반환
    finally:
        db.close() # db 세션 종료