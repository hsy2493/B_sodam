# app/services/qna_service.py
from datetime import date
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.kjh_models import Qna, ChatLog
from sqlalchemy import func

class QnaService:
    def __init__(self, db: Session):
        self.db = db

    def create_or_update_qna(self, chat_log_id: str, question: str, answer: str) -> Dict[str, Any]:
        """기존 QNA 확인 후 업데이트 또는 삽입. 같은 날 같은 내용은 무시."""
        from sqlalchemy.exc import IntegrityError
        from time import sleep

        try:
            current_date = date.today()

            # 1. 기존 동일 QnA 찾기
            existing_qna = self.db.query(Qna).filter(
                Qna.chat_log_id == chat_log_id,
                Qna.question == question,
                Qna.answer == answer
            ).order_by(Qna.upt_date.desc()).first()

            if existing_qna:
                if existing_qna.upt_date == current_date:
                    return {
                        "qna_id": existing_qna.qna_id,
                        "question": question,
                        "answer": answer,
                        "upt_date": existing_qna.upt_date.strftime("%Y-%m-%d")
                    }
                else:
                    existing_qna.upt_date = current_date
                    self.db.commit()
                    return {
                        "qna_id": existing_qna.qna_id,
                        "question": question,
                        "answer": answer,
                        "upt_date": current_date.strftime("%Y-%m-%d")
                    }

            # 2. 새로운 QnA 삽입 (중복 방지 로직 포함)
            for _ in range(3):  # 최대 3번 재시도
                last_qna = self.db.query(Qna.qna_id).filter(Qna.qna_id.like('b%')) \
                    .order_by(Qna.qna_id.desc()).first()

                if last_qna:
                    try:
                        current_num = int(last_qna.qna_id.replace('b', ''))
                        new_qna_id = f'b{str(current_num + 1).zfill(4)}'
                    except ValueError:
                        new_qna_id = 'b0001'
                else:
                    new_qna_id = 'b0001'

                new_qna = Qna(
                    qna_id=new_qna_id,
                    chat_log_id=chat_log_id,
                    question=question,
                    answer=answer,
                    reg_date=current_date,
                    upt_date=current_date
                )
                 # commit추가
                self.db.add(new_qna)
                try:
                    self.db.commit()
                    return {
                        "qna_id": new_qna_id,
                        "question": question,
                        "answer": answer,
                        "upt_date": current_date.strftime("%Y-%m-%d")
                    }
                except IntegrityError:
                    self.db.rollback()
                    sleep(0.1)  # 잠시 대기 후 재시도

            # 3회 실패 시 에러
            raise Exception("Failed to generate unique qna_id after multiple attempts.")

        except Exception as e:
            self.db.rollback()
            print(f"Error in create_or_update_qna: {e}")
            raise e


    def get_qna_by_chat_log_id(self, chat_log_id: str) -> List[Dict[str, Any]]:
        """특정 chat_log_id에 해당하는 모든 QNA 데이터 가져오기"""
        try:
            results = self.db.query(Qna).filter(Qna.chat_log_id == chat_log_id).order_by(Qna.reg_date.desc()).all()
            
            # 날짜 객체를 "YYYY-MM-DD" 문자열로 변환
            formatted_results = []
            for qna in results:
                formatted_row = {
                    "chat_log_id": qna.chat_log_id,
                    "qna_id": qna.qna_id,
                    "question": qna.question,
                    "answer": qna.answer,
                    "reg_date": qna.reg_date.strftime("%Y-%m-%d") if qna.reg_date else None,
                    "upt_date": qna.upt_date.strftime("%Y-%m-%d") if qna.upt_date else None
                }
                formatted_results.append(formatted_row)
                
            return formatted_results
            
        except Exception as e:
            print(f"Error getting QNA data: {e}")
            return []

    def get_qna_by_email(self, mem_email: str) -> List[Dict[str, Any]]:
        """특정 이메일에 해당하는 모든 QNA 데이터 가져오기 (chat_log 테이블 JOIN)"""
        try:
            results = self.db.query(Qna).join(ChatLog, Qna.chat_log_id == ChatLog.chat_log_id).filter(
                ChatLog.mem_email == mem_email
            ).order_by(Qna.reg_date.desc()).all()

            # 날짜 객체를 "YYYY-MM-DD" 문자열로 변환
            formatted_results = []
            for qna in results:
                formatted_row = {
                    "chat_log_id": qna.chat_log_id,
                    "qna_id": qna.qna_id,
                    "question": qna.question,
                    "answer": qna.answer,
                    "reg_date": qna.reg_date.strftime("%Y-%m-%d") if qna.reg_date else None,
                    "upt_date": qna.upt_date.strftime("%Y-%m-%d") if qna.upt_date else None
                }
                formatted_results.append(formatted_row)

            return formatted_results

        except Exception as e:
            print(f"Error getting QNA data by email: {e}")
            return []