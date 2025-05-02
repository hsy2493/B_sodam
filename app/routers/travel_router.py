# app/routers/travel_router.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from app.schema.travel_schema import JHRequestDto, JHResponse, JHRequestDto2, JHResponse2, JHRequestDto3, JHResponse3
from app.services.model_service import TravelModelService
from app.services.chat_service import ChatService
from app.services.qna_service import QnaService
from app.database.database import get_db
from sqlalchemy.orm import Session
from typing import List
import re
import json

router = APIRouter()
model_service = TravelModelService()
templates = Jinja2Templates(directory="app/templates")

def get_chat_service(db: Session = Depends(get_db)):
    return ChatService(db)

def get_qna_service(db: Session = Depends(get_db)):
    return QnaService(db)



@router.post("/page04/message", response_model=JHResponse)
async def process_jh_message(
    request: JHRequestDto,
    chat_service: ChatService = Depends(get_chat_service),
    qna_service: QnaService = Depends(get_qna_service)
):
    """
    Spring Boot 연동용 API 엔드포인트
    - 메시지와 이메일 처리
    - chat_log 생성 없이, 기존 이메일 기반 최신 chat_log에 QNA 저장
    - 모든 로그 및 관련 QNA 반환
    """
    try:
        message = request.message
        email = request.email
         # commit추가
        # 모델 응답 생성
        result = model_service.process_chatbot_query(message)
        recommendations_text = "\n".join([f"- {item}" for item in result["recommendations"]])
        additional_info = result.get("additional_info", "")
        response_text = f"{recommendations_text}\n\n{additional_info}" if additional_info else recommendations_text

        response_data = {"response": response_text}

        if email:
            try:
                # ✅ 기존 chat_log 중 최신 항목 조회
                latest_log = chat_service.get_latest_chat_log_by_email(email)
                chat_log_id = latest_log.get("chat_log_id") if latest_log else None

                # ✅ QNA 생성
                if chat_log_id:
                    qna_service.create_or_update_qna(
                        chat_log_id=chat_log_id,
                        question=message,
                        answer=response_text
                    )

                # 전체 로그 및 QNA 반환
                all_chat_logs = chat_service.get_chat_logs_by_email(email)
                all_qna_for_email = qna_service.get_qna_by_email(email)

                if all_chat_logs:
                    response_data["titles"] = [log.get("title") for log in all_chat_logs if log.get("title")]
                    response_data["upt_dates"] = [log.get("upt_date") for log in all_chat_logs if log.get("upt_date")]
                    response_data["chat_logs"] = all_chat_logs

                if all_qna_for_email:
                    response_data["questions"] = [qna.get("question") for qna in all_qna_for_email if qna.get("question")]
                    response_data["answers"] = [qna.get("answer") for qna in all_qna_for_email if qna.get("answer")]

                # 현재 chat_log_id의 QNA 필터링
                if chat_log_id:
                    current_qna_data = qna_service.get_qna_by_chat_log_id(chat_log_id)
                    if current_qna_data:
                        response_data["qna_data"] = current_qna_data

            except Exception as e:
                print(f"데이터 처리/조회 실패: {str(e)}")

        return JHResponse(**response_data)

    except Exception as e:
        error_message = f"오류가 발생했습니다: {str(e)}"
        return JHResponse(response=error_message)


    
@router.post("/page3/message", response_model=JHResponse2)
async def process_jh_message2(
    request: JHRequestDto2,
    chat_service: ChatService = Depends(get_chat_service),
    qna_service: QnaService = Depends(get_qna_service)
):
    """
    Spring Boot 연동용 API 엔드포인트 (조회 전용)
    - Gemini 응답만 생성
    - email을 통해 chat_log 및 qna 데이터 조회
    - high_loc를 기반으로 chat_log 자동 생성
    """
    try:
        message = request.message
        email = request.email
        high_loc2 = request.high_loc2  # 추가: high_loc 값 추출

        # 모델 응답 생성 (위치 정보 포함 가능성)
        result = model_service.process_Area_query(message)
        recommendations_text = "\n".join([f"- {item}" for item in result["recommendations"]])
        additional_info = result.get("additional_info", "")
        response_text = f"{recommendations_text}\n\n{additional_info}" if additional_info else recommendations_text

        # 응답 데이터 초기화
        response_data = {
            "response": response_text,
            "latitude": result.get("latitude"),
            "longitude": result.get("longitude"),
        }
        
        #print("제미나이 답변 : "+response_text)
        
        # gemini 답변에서 JSON 추출
        match = re.search(r'\{[\s\S]*\}', response_text)
        area_list_json_str = match.group() if match else None
        
        #print("해당 답변 json 처리 : "+area_list_json_str)
                
        # json 문자열 json list로 전환
        # print("지역리스트 json 처리 시작")
        try:
            area_list = json.loads(area_list_json_str)  # dict
            # print("지역리스트 json: ", area_list_json)
            # area_list = AreaLists(**area_list_json["items"])
            # print("AreaLists 객체: ", area_list)
        except Exception as e:
            area_list = {}
            print("지역리스트 json 처리중 에러 발생:", e)
              

        if email:
            try:
                # ✅ high_loc로 chat_log 생성
                if high_loc2:
                    created_log = chat_service.update_chat_log(mem_email=email, answer=high_loc2, choose_val=request, area_list=area_list)
                    response_data["created_chat_log"] = created_log

                
                # 모든 데이터 조회 및 리스트 생성
                all_chat_logs = chat_service.get_chat_logs_by_email(email)            

                if all_chat_logs:
                    response_data["titles"] = [log.get("title") for log in all_chat_logs if log.get("title")]
                    response_data["upt_dates"] = [log.get("upt_date") for log in all_chat_logs if log.get("upt_date")]
                    response_data["chat_logs"] = all_chat_logs

                

               
                    

            except Exception as e:
                print(f"데이터 조회 실패 (page3): {str(e)}")

        return JHResponse2(**response_data)

    except Exception as e:
        error_message = f"오류가 발생했습니다: {str(e)}"
        return JHResponse2(response=error_message)

@router.post("/page5/message", response_model=JHResponse3)
async def process_jh_message3(
    request: JHRequestDto3,
    chat_service: ChatService = Depends(get_chat_service),
    qna_service: QnaService = Depends(get_qna_service)
):
    try:
        message = request.message  # 이 값은 chat_log_id
        email = request.email

        response_data = {"response": message}

        # 1. email이 존재하면 해당 유저의 모든 chat_log 반환
        if email:
            chat_logs = chat_service.get_chat_logs_by_email(email)
            if chat_logs:
                response_data["chat_logs"] = chat_logs
                response_data["titles"] = [log["title"] for log in chat_logs]
                response_data["upt_dates"] = [log["upt_date"] for log in chat_logs]

        # 2. message(chat_log_id)가 존재하면 해당 ID로 QnA 조회
        if message:
            matched_qna_list = qna_service.get_qna_by_chat_log_id(message)
            if matched_qna_list:
                response_data["qna_data"] = matched_qna_list
        return JHResponse3(**response_data)

    except Exception as e:
        error_message = f"오류가 발생했습니다: {str(e)}"
        return JHResponse3(response=error_message)


