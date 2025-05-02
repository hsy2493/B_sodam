# main.py

# FastAPI
from fastapi import FastAPI
from app.database.database import Base,engine
import uvicorn # server
from fastapi.middleware.cors import CORSMiddleware # CORS 미들웨어 import

app = FastAPI()

origins = [
    "http://localhost:8080",  # 클라이언트 Origin (현재 HTML 파일을 여는 주소)
    "http://localhost:8000",  # FastAPI 서버 Origin
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
    "*",  # 모든 Origin 허용 (개발 환경에서 편리하지만, 실제 배포 시에는 보안상 특정 Origin만 허용하는 것이 좋습니다.)
] #localhost 8080, 8000 보안허용

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

Base.metadata.create_all(bind=engine)

# 세션 관리
from starlette.middleware.sessions import SessionMiddleware # 세션 관리 미들웨어 
from app.key.secretkey import SESSION_KEY  # 세션 key 정보 
app.add_middleware(SessionMiddleware, secret_key=SESSION_KEY) # 세션 지정 

# router 
from app.routers import member_router,auth_router # member router
app.include_router(member_router.router) 
app.include_router(auth_router.router) 

"""유찬우"""
# 선택값 CRUD 라우터
from app.routers import choose_val_router
app.include_router(choose_val_router.choose_router)
"""유찬우 끝"""
"""권정현"""
from app.routers import travel_router
app.include_router(travel_router.router)
"""권정현 끝"""
# FAST 실행명령어 자동 실행 (main 함수)   
# http://127.0.0.1:8000/docs
if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
    # 서버 종료 단축키 : ctrl + c 