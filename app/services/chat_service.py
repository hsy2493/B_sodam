# app/services/chat_service.py
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from app.models.kjh_models import ChatLog
from app.schema.travel_schema import JHRequestDto2
from app.models.ycw_models import Choose_val_Model, Area_list_Model


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def update_chat_log(self, mem_email: str, answer: str, choose_val: JHRequestDto2, area_list: dict) -> Optional[Dict[str, Any]]:
        """
        answer 값을 기반으로 title은 answer + ' 여행' 으로 지정.
        기존 로그 여부에 상관없이 매번 새로운 chat_log 생성.
        """
        try:
            current_date2 = datetime.now()
            current_date = date.today()
            # 1. title 생성 (answer + ' 여행')
            if answer:
                trimmed_title = (answer.strip().replace("\n", " ") + " 여행")[:100]
            else:
                trimmed_title = "No Title 여행"

            # 2. chat_log_id 생성
            last_log = self.db.query(ChatLog.chat_log_id).order_by(ChatLog.chat_log_id.desc()).first()
            if last_log and last_log.chat_log_id.startswith('a'):
                try:
                    last_id_num = int(last_log.chat_log_id[1:])
                    new_id_num = last_id_num + 1
                    new_chat_log_id = f"a{new_id_num:04d}"
                except ValueError:
                    new_chat_log_id = 'a0001'
            else:
                new_chat_log_id = 'a0001'

            # 3. 새로운 로그 생성
            new_log = ChatLog(
                chat_log_id=new_chat_log_id,
                mem_email=mem_email,
                title=trimmed_title,
                reg_date=current_date2,
                upt_date=current_date
            )
            self.db.add(new_log)
            
            db_choose_val = Choose_val_Model(
                chat_log_id=new_chat_log_id,
                high_loc=choose_val.high_loc2,
                low_loc=choose_val.low_loc,
                theme1=choose_val.theme1,
                theme2=choose_val.theme2,
                theme3=choose_val.theme3,
                theme4=choose_val.theme4,
                days=choose_val.days)
            self.db.add(db_choose_val)
            
            for a in area_list["items"]["item"]:
                db_area_list = Area_list_Model(
                    chat_log_id = new_chat_log_id,
                    title = a["title"],
                    mapx = a["mapx"],
                    mapy = a["mapy"],
                    contenttypeid = a["contenttypeid"],
                    firstimage = a["firstimage"],
                    firstimage2 = a["firstimage2"],
                    tel = a["tel"],
                    addr1 = a["addr1"],
                    addr2 = a["addr2"])
                self.db.add(db_area_list)
            
            self.db.commit()
            
            return {
                "chat_log_id": new_chat_log_id,
                "title": trimmed_title,
                "upt_date": current_date.strftime("%Y-%m-%d")
            }

        except Exception as e:
            self.db.rollback()
            print(f"Error in update_chat_log: {e}")
            raise e

        
    def get_chat_logs_by_email(self, mem_email: str) -> List[Dict[str, Any]]:
        """특정 이메일의 모든 채팅 로그 가져오기"""
        try:
            results = self.db.query(ChatLog).filter(ChatLog.mem_email == mem_email).order_by(ChatLog.reg_date.desc()).all()
            
            # 날짜 객체를 "YYYY-MM-DD" 문자열로 변환
            formatted_results = []
            for log in results:
                formatted_row = {
                    "chat_log_id": log.chat_log_id,
                    "mem_email": log.mem_email,
                    "title": log.title,
                    "reg_date": log.reg_date.strftime("%Y-%m-%d %H:%M") if log.reg_date else None,
                    "upt_date": log.upt_date.strftime("%Y-%m-%d") if log.upt_date else None
                }
                formatted_results.append(formatted_row)
                
            return formatted_results
            
        except Exception as e:
            print(f"Error getting chat logs: {e}")
            return []
    def get_latest_chat_log_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        try:
            log = self.db.query(ChatLog).filter(
                ChatLog.mem_email == email
            ).order_by(ChatLog.chat_log_id.desc()).first()

            if log:
                return {
                    "chat_log_id": log.chat_log_id,
                    "title": log.title,
                    "upt_date": log.upt_date.strftime("%Y-%m-%d")
                }

            return None

        except Exception as e:
            print(f"get_latest_chat_log_by_email Error: {e}")
            return None
    def get_chat_log_by_id(self, chat_log_id: str) -> Optional[Dict[str, Any]]:
        """chat_log_id로 특정 채팅 로그를 조회"""
        try:
            log = self.db.query(ChatLog).filter(ChatLog.chat_log_id == chat_log_id).first()

            if log:
                return {
                    "chat_log_id": log.chat_log_id,
                    "mem_email": log.mem_email,
                    "title": log.title,
                    "reg_date": log.reg_date.strftime("%Y-%m-%d %H:%M") if log.reg_date else None,
                    "upt_date": log.upt_date.strftime("%Y-%m-%d") if log.upt_date else None
                }
            return None

        except Exception as e:
            print(f"Error in get_chat_log_by_id: {e}")
            return None