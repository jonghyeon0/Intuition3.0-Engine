import os
from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

# 보안을 위해 키는 환경변수에서 읽는다
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/analyze/{company_code}")
async def get_tci_analysis(company_code: str):
    # 고정/유동 DB 로직이 여기서 가동된다
    model = genai.GenerativeModel('gemini-1.5-pro')
    # T(과거 궤적), C(물리적 확신), I(미래 리스크)를 해부하는 프롬프트
    prompt = f"기업 {company_code}의 최신 뉴스 및 수급 데이터를 분석하여 T, C, I 점수를 산출하라."
    response = model.generate_content(prompt)
    return {"status": "success", "result": response.text}
