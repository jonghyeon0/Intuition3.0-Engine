import os
from fastapi import FastAPI, BackgroundTasks
import google.generativeai as genai
import redis

app = FastAPI()

# 1. 환경 설정 (Render 환경변수 연동)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Redis는 Render에서 제공하는 내부 URL을 사용한다
cache = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

@app.get("/pre-analyze/{code}")
async def pre_analyze(code: str, tasks: BackgroundTasks):
    """유저가 클릭하기 전 미리 연산해서 Redis에 박아두는 로직"""
    if not cache.exists(code):
        tasks.add_task(run_tci_engine, code)
    return {"status": "warming_up"}

@app.get("/analyze/{code}")
async def analyze(code: str):
      # --- 여기서부터 22행 시작 ---
    """더미 데이터를 즉시 반환하여 시안을 확인하는 로직"""
    dummy_data = {
        "code": code,
        "total_score": "88",
        "T_score": "92",
        "C_score": "75",
        "I_score": "95",
        "insight": "자본의 결속력이 임계점에 도달했습니다. 정보 발행자의 의도가 가격 지지선과 일치합니다.",
        "process_t": "과거 5년간의 매집 패턴과 현재 거래량 폭발의 궤적이 92% 일치함.",
        "process_c": "공시된 설비 투자 내역과 기사 내 언급된 생산 능력이 물리적으로 정합함.",
        "process_i": "대주주 지분 변동 추이 역산 결과, 하방 리스크 필터링이 완료된 매집 의도 포착."
    }
    return {"status": "success", "data": dummy_data}
    # --- 여기까지 27행 끝 ---


def run_tci_engine(code):
    model = genai.GenerativeModel('gemini-3.0-pro')
    # 팀장의 TCI 공식 주입
    prompt = f"기업 {code}에 대해 S=T*0.5+C*0.3+I*0.2 공식을 적용해 독설 리포트를 써라."
    response = model.generate_content(prompt)
    cache.setex(code, 300, response.text) # 5분간 유효
    return response.text
