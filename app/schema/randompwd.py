import random
import string

class RandomPwd(): # 랜덤 비밀번호 생성
    upper = string.ascii_uppercase # 대문자
    lower = string.ascii_lowercase # 소문자 
    digit = string.digits # 숫자 
    str = upper + lower + digit # 대문자, 소문자, 숫자 조합
    
    def random_password(self, length=12):
        return ''.join(random.choice(self.str) for _ in range(length))
    
    