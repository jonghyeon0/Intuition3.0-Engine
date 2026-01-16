import os
from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

# 환경변수에서 키를 읽어옴 (보안 필수)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/analyze/{company_code}")
async def get_analysis(company_code: str):
    # 여기서 미래에셋 API 호출 로직이 연결됨
    model = genai.GenerativeModel('gemini-3.0-pro') # 최신 모델 사용
    response = model.generate_content(f"{company_code} 기업의 실시간 수급 및 TCI 분석을 실시하라.")
    return {"status": "success", "analysis": response.text}
