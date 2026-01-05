from __future__ import annotations
import time
from src.llm.gemini_client import get_client, get_model_name
from src.llm.oibook_prompt import build_oibook_prompt

def generate_oibook(company: str, fulltext: str, *, max_retries: int = 3) -> str:
    client = get_client()
    model = get_model_name()
    prompt = build_oibook_prompt(company=company, fulltext=fulltext)

    last_err = None
    for i in range(max_retries):
        try:
            resp = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            text = getattr(resp, "text", None) or ""
            text = text.strip()
            if not text:
                raise RuntimeError("Gemini 응답이 비어있습니다.")
            return text
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (2 ** i))
    raise RuntimeError(f"Gemini 호출 실패: {last_err}")
