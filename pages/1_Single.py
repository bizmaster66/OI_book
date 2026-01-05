import streamlit as st
from src.ui.styles import inject_global_styles
from src.ui.oibook_view import render_oibook_cards
from src.llm.oibook_generator import generate_oibook
from src.llm.gemini_client import get_model_name
from src.store.history_store import append_history

inject_global_styles()
st.title("Single: Full text → OI Book")

colA, colB = st.columns([2, 1], gap="large")

with colA:
    company = st.text_input("회사명", placeholder="예: 와이앤지 / 메텔 / ...")
    mode = st.radio("입력 방식", ["텍스트 붙여넣기", "파일 업로드(.txt/.md)"], horizontal=True)

    fulltext = ""
    source_name = "paste"
    if mode == "텍스트 붙여넣기":
        fulltext = st.text_area("Full text", height=280, placeholder="여기에 Full text를 붙여넣으세요.")
    else:
        up = st.file_uploader("Full text 파일", type=["txt", "md"])
        if up:
            source_name = up.name
            fulltext = up.read().decode("utf-8", errors="ignore")

with colB:
    st.markdown('<span class="oi-pill">Gemini</span><span class="oi-pill">.env</span><span class="oi-pill">Markdown</span>', unsafe_allow_html=True)
    st.caption("IR Full text에 없는 사실/수치는 작성하지 않도록 강제합니다.")
    gen = st.button("OI Book 생성", type="primary", use_container_width=True)

if gen:
    if not company.strip():
        st.error("회사명을 입력하세요.")
        st.stop()
    if not fulltext.strip():
        st.error("Full text를 입력/업로드하세요.")
        st.stop()

    with st.spinner("Gemini로 OI Book 생성 중..."):
        md = generate_oibook(company.strip(), fulltext)

    append_history(
        company=company.strip(),
        source_name=source_name,
        fulltext=fulltext,
        model=get_model_name(),
        oibook_md=md,
    )

    st.success("생성 완료! 아래에서 확인/다운로드하세요.")

    tab_design, tab_md = st.tabs(["디자인 뷰", "마크다운"])
    with tab_design:
        render_oibook_cards(md, title_override=f"{company.strip()} OI Book")
    with tab_md:
        st.code(md, language="markdown")

    st.download_button(
        "마크다운 다운로드(.md)",
        data=md.encode("utf-8"),
        file_name=f"{company.strip()}_oi_book.md",
        mime="text/markdown",
        use_container_width=True,
    )

    with st.expander("원문 마크다운 보기"):
        st.code(md, language="markdown")
