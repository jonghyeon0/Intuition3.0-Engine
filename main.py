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
    """유저가 클릭했을 때 캐시된 결과를 즉시 반환"""
    result = cache.get(code)
    if result:
        return {"status": "success", "data": result.decode('utf-8')}
    # 만약 캐시에 없으면 즉시 연산 (Safety Net)
    return {"status": "success", "data": run_tci_engine(code)}

def run_tci_engine(code):
    model = genai.GenerativeModel('gemini-3.0-pro')
    # 팀장의 TCI 공식 주입
    prompt = f"기업 {code}에 대해 S=T*0.5+C*0.3+I*0.2 공식을 적용해 독설 리포트를 써라."
    response = model.generate_content(prompt)
    cache.setex(code, 300, response.text) # 5분간 유효
    return response.text
