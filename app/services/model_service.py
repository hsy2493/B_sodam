from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from typing import List, Tuple, Dict, Any ,Optional
import requests
import re
import random
import os
from concurrent.futures import ThreadPoolExecutor
import unicodedata

class TravelModelService:
    def __init__(self):
        """
        여행 추천 모델 서비스 초기화
        - 다국어 지원 Sentence-BERT 모델 사용
        """
        self.model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
        
        # 스프링부트 백엔드 API 기본 URL
        self.spring_api_url = "http://localhost:8080/api"
        
        # 샘플 추천 템플릿 (실제 구현시 모델의 출력으로 대체)
        self.recommendation_templates = {
            "서울": {
                "당일": {
                    "문화": ["경복궁 투어", "인사동 문화거리", "북촌한옥마을"],
                    "자연": ["남산공원", "서울숲", "한강공원"],
                    "맛집": ["광장시장 투어", "이태원 맛집거리", "연남동 맛집"]
                },
                "1박2일": {
                    "문화": ["고궁 순례", "박물관 투어", "공연 관람"],
                    "자연": ["북한산 등산", "서울숲 피크닉", "한강 자전거"],
                    "맛집": ["먹방 투어", "야시장 탐방", "카페 투어"]
                }
            },
            "부산": {
                "당일": {
                    "문화": ["감천문화마을", "국제시장", "용두산공원"],
                    "자연": ["해운대", "광안리", "태종대"],
                    "맛집": ["자갈치시장", "부산어묵 투어", "씨푸드 맛집"]
                },
                "1박2일": {
                    "문화": ["영도 문화투어", "부산 영화거리", "차이나타운"],
                    "자연": ["오륙도 스카이워크", "동백섬", "송정해수욕장"],
                    "맛집": ["서면 맛집거리", "해운대 회 투어", "부산 야시장"]
                }
            }
        }

        # Set up the environment variable for the Gemini API key
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if not self.gemini_api_key:
            # 환경 변수가 설정되지 않은 경우, 직접 API 키 등록
            self.gemini_api_key = "AIzaSyBJocl_THRDmgFNGg5hJ-ONiqdSRwVaFO8"
            os.environ["GEMINI_API_KEY"] = self.gemini_api_key

        if not self.gemini_api_key:
            raise ValueError("Gemini API 키가 설정되지 않았습니다.")

        # Initialize a thread pool for asynchronous processing
        self.executor = ThreadPoolExecutor(max_workers=5)

    def _get_embedding(self, text: str) -> np.ndarray:
        """텍스트를 임베딩 벡터로 변환"""
        return self.model.encode(text)

    def _combine_keywords(self, location: str, schedule: str, theme: str) -> str:
        """키워드들을 하나의 문장으로 결합"""
        return f"{location}에서 {schedule} 동안 {theme} 여행"

    def _calculate_confidence(self, embeddings: List[np.ndarray]) -> float:
        """신뢰도 점수 계산 (코사인 유사도 기반)"""
        if len(embeddings) < 2:
            return 1.0
            
        similarities = []
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                similarity = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )
                similarities.append(similarity)
                
        return float(np.mean(similarities))

    def get_recommendations(self, location: str, schedule: str, theme: str) -> Tuple[List[str], float]:
        """
        키워드 기반 여행 추천
        
        Args:
            location: 지역 키워드
            schedule: 일정 키워드
            theme: 테마 키워드
            
        Returns:
            Tuple[List[str], float]: (추천 목록, 신뢰도 점수)
        """
        try:
            # SpringBoot API 호출
            try:
                # Spring Boot 백엔드에서 추천 데이터 가져오기
                data = {
                    "location": location,
                    "schedule": schedule,
                    "theme": theme
                }
                response = requests.post(f"{self.spring_api_url}/recommendations", json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    return result["recommendations"], result["confidenceScore"]
            except Exception as api_error:
                print(f"Spring API 호출 실패, 로컬 추천 사용: {api_error}")
            
            # API 호출 실패 시 로컬 로직으로 대체
            # 1. 각 키워드의 임베딩 생성
            embeddings = [
                self._get_embedding(location),
                self._get_embedding(schedule),
                self._get_embedding(theme)
            ]
            
            # 2. 신뢰도 점수 계산
            confidence = self._calculate_confidence(embeddings)
            
            # 3. 추천 생성 (실제 구현에서는 모델 기반 추천으로 대체)
            recommendations = self.recommendation_templates.get(location, {}).get(schedule, {}).get(theme, [])
            
            # 추천이 없는 경우 기본 추천
            if not recommendations:
                recommendations = [
                    f"{location} {theme} 명소 추천",
                    f"{schedule} 코스 추천",
                    f"{theme} 중심 여행 코스"
                ]
                confidence *= 0.7  # 기본 추천의 경우 신뢰도 감소
            
            return recommendations, confidence
            
        except Exception as e:
            # 오류 발생시 기본 추천과 낮은 신뢰도 반환
            return [
                "일반적인 관광지 추천",
                "맛집 탐방",
                "문화 체험"
            ], 0.3
            
    def analyze_with_gemini(self, query: str) -> str:
        """Gemini API를 사용하여 쿼리 분석 및 응답 생성"""
        try:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': self.gemini_api_key
            }
            data = {"contents": [{"parts": [{"text": query}]}]}
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']

        except Exception as e:
            raise Exception(f"Gemini 분석 중 오류 발생: {str(e)}")

    def process_chatbot_query(self, query: str) -> Dict[str, Any]:
        """사용자 쿼리를 처리하여 Gemini API를 사용하여 응답 생성"""
        try:
            # Use a thread pool to handle the request 
            prompt = "간단하고 짧게 대답해주세요. 답변에 이모티콘이나 이모지등을 쓰지말아줘 질문: " + query
            future = self.executor.submit(self.analyze_with_gemini, prompt)
            gemini_response = future.result(timeout=10)  # Set a timeout for the response
            combined_response = f"Gemini: {gemini_response}"
            # commit추가
            return {
                "recommendations": [combined_response],
                "confidence_score": 0.9,
                "additional_info": "Gemini API 응답"
            }
        except Exception as e:
            return {
                "recommendations": ["오류가 발생했습니다. 다시 시도해주세요."],
                "confidence_score": 0.1,
                "additional_info": f"오류: {str(e)}"
            }
            
    def process_Area_query(self, query: str) -> Dict[str, Any]:
        """사용자 쿼리를 처리하여 Gemini API를 사용하여 응답 생성"""
        try:
            prompt = """
                다음은 지역리스트입니다. 
                contenttypeid가 32면 해당 지역은 숙박업소입니다.
                contenttypeid가 39면 해당 지역은 음식점입니다.
                이 지역간에 거리가 가깝고 
                contenttypeid가 겹치지 않는 서로 다른 추천여행지를
                서로간의 거리를 고려하고 숙박업소와 음식점을 제외하여
                날짜가 1이면 3곳, 2이면 5곳, 3이면 7곳을 추천해주세요.
                날짜가 2이면 숙박업소를 1곳, 3이면 2곳을 추가하여 추천해주세요.
                날짜가 1이면 음식점을 2곳, 2이면 4곳, 3이면 6곳을 추가하여 추천해주세요.
                받은 지역리스트에서 음식점의 수가 부족하면 그만큼 다른 여행지를 추가로 추천해주세요.
                출력형식은 받은 형식을 참고하여 다음 json형식을 지켜서 출력해주세요.
                {
                    "items": {
                        "item":     [
                            {
                                "title": "",
                                "mapx": "",
                                "mapy": "",
                                "contenttypeid": "",
                                "firstimage": "",
                                "firstimage2": "",
                                "tel": "",
                                "addr1": "",
                                "addr2": ""
                            },...
                        ]
                    }
                }
                모든 json의 벨류값은 String타입으로 보내주세요.
                지역리스트: 
                """+ query
                # 만약 받은 데이터에 null값이 있다면 공백문자열("")로 보내주세요
                # 당일여행일때 3곳 1박2일일때 5곳 2박3일일때 10곳만 추천하여 알려주세요.
                # 날짜가 지역리스트에 포함이 안되었다면 5개를 출력하고 포함안됨을 출력해주세요
            future = self.executor.submit(self.analyze_with_gemini, prompt)
            gemini_response = future.result(timeout=10)

            # 전체 응답을 문자열로 처리
            combined_response = f"Gemini: {gemini_response}"

            # 응답 문자열에서 각 추천 항목만 추출 (JSON 객체 단위)
            items = re.findall(r'{.*?}', gemini_response, re.DOTALL)

            # 하나를 무작위로 선택
            selected = random.choice(items) if items else ""

            # 위도 경도 초기값
            latitude: Optional[float] = None
            longitude: Optional[float] = None

            # mapx, mapy 추출 시 정규표현식 사용
            mapx_match = re.search(r'"mapx"\s*:\s*([\d.]+)', selected)
            mapy_match = re.search(r'"mapy"\s*:\s*([\d.]+)', selected)

            if mapx_match:
                try:
                    longitude = float(mapx_match.group(1))
                except ValueError:
                    pass
            if mapy_match:
                try:
                    latitude = float(mapy_match.group(1))
                except ValueError:
                    pass

            return {
                "recommendations": [combined_response],
                "selected_place": selected,
                "latitude": latitude,
                "longitude": longitude,
                "confidence_score": 0.9,
                "additional_info": "문자열 응답에서 무작위 장소 선택 및 좌표 추출"
            }

        except Exception as e:
            return {
                "recommendations": ["오류가 발생했습니다. 다시 시도해주세요."],
                "selected_place": "",
                "latitude": None,
                "longitude": None,
                "confidence_score": 0.1,
                "additional_info": f"오류: {str(e)}"
            }