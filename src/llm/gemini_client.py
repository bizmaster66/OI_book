import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # .env 로드

def get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다. .env에 GEMINI_API_KEY를 넣어주세요.")
    return genai.Client(api_key=api_key)
