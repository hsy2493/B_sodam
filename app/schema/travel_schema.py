from datetime import date # 추가
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TravelKeywordRequest(BaseModel):
    """여행 키워드 요청 스키마"""
    location: str  # 지역 키워드
    schedule: str  # 일정 키워드
    theme: str    # 테마 키워드

class ChatbotRequest(BaseModel):
    """챗봇 질문 요청 스키마"""
    query: str  # 사용자 질문

class JHRequestDto(BaseModel):
    """JH 서비스 요청 스키마 (Spring Boot 연동용)"""
    message: str  # 사용자 메시지 (필수)
    email: Optional[str] = None  # 사용자 이메일 (선택)

class ChatLogItem(BaseModel):
    """채팅 로그 항목"""
    chat_log_id: str # 테이블의 chat_log_id 컬럼 (a0001/a0002 값 또는 DB 자동 생성 ID)
    mem_email: str
    title: str
    reg_date: str
    upt_date: str

class QnaItem(BaseModel):
    """QNA 항목"""
    chat_log_id: str
    qna_id: str
    question: str
    answer: str
    reg_date: str
    upt_date: str

class JHResponse(BaseModel):
    """JH 서비스 응답 스키마 (Spring Boot 연동용)"""
    response: str  # 응답 메시지 (필수)
    upt_date: Optional[str] = None # 업데이트 날짜 (선택)
    title: Optional[str] = None  # 채팅 제목 (선택)
    question: Optional[str] = None  # QNA 질문 내용 (선택)
    answer: Optional[str] = None  # QNA 답변 내용 (선택)
    chat_logs: Optional[List[ChatLogItem]] = None  # 모든 채팅 로그 (선택)
    qna_data: Optional[List[QnaItem]] = None  # 모든 QNA 데이터 (선택)

class JHRequestDto2(BaseModel):
    """JH 서비스 요청 스키마 2 (Spring Boot 연동용) - 위치 정보 포함"""
    message: str # 사용자 메시지 (필수)
    email: Optional[str] = None # 사용자 이메일 (선택)
    high_loc2: str
    chat_log_id:Optional[str] = None
    low_loc: Optional[str] = None
    theme1: str
    theme2: str
    theme3: Optional[str] = None
    theme4: Optional[str] = None
    days: int
    
class JHResponse2(BaseModel):
    """JH 서비스 응답 스키마 2 (Spring Boot 연동용) - 위치 정보 포함"""
    response: str  # 응답 메시지 (필수)
    latitude: Optional[float] = None  # 위도
    longitude: Optional[float] = None # 경도
    # JHResponse와 동일한 필드 추가
    upt_date: Optional[str] = None # 업데이트 날짜 (선택)
    title: Optional[str] = None  # 채팅 제목 (선택)
    question: Optional[str] = None  # QNA 질문 내용 (선택)
    answer: Optional[str] = None  # QNA 답변 내용 (선택)
    chat_logs: Optional[List[ChatLogItem]] = None  # 모든 채팅 로그 (선택)
    qna_data: Optional[List[QnaItem]] = None  # 모든 QNA 데이터 (선택)
    
class JHRequestDto3(BaseModel):
    """JH 서비스 요청 스키마 2 (Spring Boot 연동용) - 위치 정보 포함"""
    message: str # 사용자 메시지 (필수)
    email: Optional[str] = None # 사용자 이메일 (선택)
    
class JHResponse3(BaseModel):
    """JH 서비스 응답 스키마 2 (Spring Boot 연동용) - 위치 정보 포함"""
    response: str  # 응답 메시지 (필수)
    # JHResponse와 동일한 필드 추가
    upt_date: Optional[str] = None # 업데이트 날짜 (선택)
    title: Optional[str] = None  # 채팅 제목 (선택)
    question: Optional[str] = None  # QNA 질문 내용 (선택)
    answer: Optional[str] = None  # QNA 답변 내용 (선택)
    chat_logs: Optional[List[ChatLogItem]] = None  # 모든 채팅 로그 (선택)
    qna_data: Optional[List[QnaItem]] = None  # 모든 QNA 데이터 (선택)
     # commit추가
class TravelRecommendationResponse(BaseModel):
    """여행 추천 응답 스키마"""
    recommendations: List[str]
    confidence_score: float
    additional_info: Optional[str] = None
    location: Optional[str] = None  # 위치 정보 (있는 경우)