from app.database.database import Base
from app.models.kjh_models import ChatLog, Qna
from app.models.sql_member import SQLMember
from app.models.ycw_models import Choose_val_Model, Area_list_Model

__all__ = ["ChatLog", "Qna", "SQLMember", "Choose_val_Model", "Area_list_Model"]
# __all__ 내부에 있는 것만 from models import *로 접근할 수 있음