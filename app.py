import streamlit as st
from src.ui.styles import inject_global_styles

st.set_page_config(page_title="OI BOOK", layout="wide")
inject_global_styles()

st.title("OI BOOK")
st.caption("Full text → OI Book (Gemini 기반 자동 생성)")

st.markdown("""
<div class="oi-card">
  <div class="oi-card-title">사용 방법</div>
  <ul>
    <li><b>Single</b>: Full text 1개 입력/업로드 → OI Book 생성</li>
    <li><b>Batch</b>: 최대 10개 파일 업로드 → 병렬 생성</li>
    <li><b>History</b>: 생성 이력 조회/다운로드</li>
  </ul>
</div>
""", unsafe_allow_html=True)
