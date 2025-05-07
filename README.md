# `소담여행` - <국내여행지 추천 AI 사이트(최종 프로젝트)> 🚗 <br>
1. 작업 기간 : 2025. 04. 02 ~2025. 05. 01
2. 주제 : 국내여행지 추천 AI 사이트
3. 목적 : 대한민국의 국내 여행지를 계획하는 고객이 온라인에서 소담여행 사이트를 활용하여 국내 여행지 추천, AI 채팅 등의 여러 기능을 이용함으로써 효율적인 국내 여행지 계획 세우는 것을 주목적으로 진행된 국내여행지 추천 AI 사이트 프로젝트 입니다.
4. 주요 기능 : 로그인, 아이디 찾기/비밀번호 찾기 페이지, 관리자 페이지, 마이 페이지 

- 역할/기능 분담 : <br>
<img width="966" alt="image" src="https://github.com/user-attachments/assets/bde60344-3385-476b-8bf5-c66d4596be03" /> <br>
- 일정표 : <br>
<img width="964" alt="image" src="https://github.com/user-attachments/assets/588cb909-083d-49e2-b2b6-3c3e74500f66" /> <br>
- 개발 환경 : <br>
<img width="967" alt="image" src="https://github.com/user-attachments/assets/f59785b8-6f66-4ed7-89aa-d4c89b9bdf40" /> <br>
- 메뉴 구조도(사이트맵) <br>
<img width="971" alt="image" src="https://github.com/user-attachments/assets/ffc6b681-f74e-4dc2-932d-c768f6a17719" /> <br>
- 요구사항 정의서 : <br>
(1) 로그인 & (3) 아이디 찾기/비밀번호 찾기 <br>
<img width="968" alt="image" src="https://github.com/user-attachments/assets/1326b6ef-7bd3-433e-9b55-dca8044eeca9" /> <br>
(4) 관리자 페이지 & (5) 마이 페이지 <br>
<img width="962" alt="image" src="https://github.com/user-attachments/assets/20effc81-3175-4c6e-a9d8-102c721bbca7" /> <br>
- 플로우 차트 <br>
(*) 전체 시스템 흐름도 <br>
<img width="684" alt="image" src="https://github.com/user-attachments/assets/ff84e7c2-52f4-4da1-aacb-bd36fa151eb2" /> <br>
(1) 로그인 & (2) 회원가입 <br>
<img width="957" alt="image" src="https://github.com/user-attachments/assets/b178b56c-5b27-4bf3-b1c8-40307b38313c" /> <br>
(3) 아이디 찾기/비밀번호 찾기 <br>
<img width="933" alt="image" src="https://github.com/user-attachments/assets/09e7e952-38a2-4679-99f1-40394a7bbd63" /> <br>
(4) 관리자 페이지 <br>
<img width="943" alt="image" src="https://github.com/user-attachments/assets/7f25f80c-f0a5-4d21-b69a-ec7725d3f288" /> <br>
(5) 마이 페이지 <br>
<img width="875" alt="image" src="https://github.com/user-attachments/assets/bb2c6aab-3d93-47f5-8c83-d5cc294b408e" /> <br>

- DB/ERD (논리적/물리적) 설계 <br>
<img width="926" alt="image" src="https://github.com/user-attachments/assets/3b60ab75-c373-446c-89f4-3046e524c051" /> <br>

- PPT 자료 : <br>
<img width="1014" alt="image" src="https://github.com/user-attachments/assets/80ef8fbf-3174-43de-91c8-bceb3cd6ad16" /> <br>
https://github.com/hsy2493/B_sodam/issues/2#issue-3043420553 <br>

- 시연 동영상 자료 : <br>
<img width="868" alt="image" src="https://github.com/user-attachments/assets/a37fa279-6950-4222-96fb-5d516df9fa6a" /> <br>
https://blog.naver.com/hsy24317/223857313806 <br>
5. 사용 툴 :
- Front-end : HTML, CSS, Javascript, JSP  <br>
- Back-end : python, Java, Spring mvc, Spring Boot, DataBase <br>
- Database : MariaDB <br>

6. 작업 인원 : 5명

7. 결과물  : <br>

## <화면 구현> <br>
(1) 로그인 <br>
1-1.) 로그인 
<img width="384" alt="image" src="https://github.com/user-attachments/assets/4e51c9c0-1f20-4e52-acd2-1b03d5c26625" /> <br> 
<설명> <br>
-아이디와 비밀번호 입력 후, 로그인 버튼 클릭 시, 로그인이 가능하다. <br>
-kakao 로그인 버튼 클릭 시, 카톡통합로그인이 가능하다. <br>
-비회원인 경우, 회원가입을 권장한다. <br>
-아이디 또는 비밀번호 분실 시, 아이디 찾기/비밀번호 찾기를 권장한다. <br>
- 로그인 - 화면구현 상세 코드 <br>
https://github.com/hsy2493/F_sodam/blob/main/src/main/webapp/WEB-INF/jsp/login.jsp <br>

(3) 아이디 찾기/비밀번호 찾기 <br>
3-1.) 아이디 찾기 <br>
<img width="358" alt="image" src="https://github.com/user-attachments/assets/b5755f45-d8c6-4dc3-a9ad-1a43fa755979" /> <br>
<설명> <br>
-이름과 전화번호 입력 후, 확인 버튼 클릭 시, 아이디 찾기가 가능하다.<br>
- 아이디 찾기 - 화면구현 상세 코드 <br>
https://github.com/hsy2493/F_sodam/blob/main/src/main/webapp/WEB-INF/jsp/find.jsp <br>

3-2.) 비밀번호 찾기 <br>
<img width="369" alt="image" src="https://github.com/user-attachments/assets/a08fd81f-cf5e-4695-9613-05edfa507939" /> <br>
-아이디(이메일) 입력 후, 임시 비밀번호 버튼 클릭 시, 임시 비밀번호 전송으로 비밀번호 찾기가 가능하다.<br>
- 비밀번호 찾기 - 화면구현 상세 코드 <br>
https://github.com/hsy2493/F_sodam/blob/main/src/main/webapp/WEB-INF/jsp/find.jsp <br>

(4) 관리자 페이지 <br>
<img width="411" alt="image" src="https://github.com/user-attachments/assets/6ceeb546-e8ee-489c-ae80-fbabc2d79792" /> <br>
-관리자 계정으로 로그인한 경우, 

(5) 마이 페이지 <br>


## <기능 구현> <br>

<b>   
8. 성과 : <br>
- 
</b>
