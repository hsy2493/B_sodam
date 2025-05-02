# app/key/secretkey.py

# import secrets
import os
import json

# 세션 처리를 위한 key 생성
# secret_key = secrets.token_hex(32)
# print(secret_key)
# 3a6333213e218c586c55bf218eaf92cada4de6628322c7a0a4dbbb7266107fd3

# 세션 처리를 위한 key 설정 
secret_keys = json.loads(os.getenv("SECRET_KEYS", '{"session_key": "default-key"}'))
SESSION_KEY = secret_keys["session_key"] # .env 파일에서 호출