import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.ui.styles import inject_global_styles
from src.ui.oibook_view import render_oibook_cards
from src.llm.oibook_generator import generate_oibook
from src.llm.gemini_client import get_model_name
from src.store.history_store import append_history

inject_global_styles()
st.title("Batch: 최대 10개 파일 병렬 생성")

st.caption("파일은 .txt 또는 .md (Full text)만 지원합니다. 최대 10개까지 동시에 분석합니다.")

files = st.file_uploader("Full text 파일 여러 개 업로드", type=["txt", "md"], accept_multiple_files=True)

default_company_rule = st.text_input(
    "회사명 추출 규칙(선택)",
    value="파일명에서 확장자 제거한 값을 회사명으로 사용",
    disabled=True,
)

run = st.button("병렬 생성 실행", type="primary", use_container_width=True)

def _company_from_filename(name: str) -> str:
    # 'ABC_fulltext.md' 같은 경우도 있으니 필요하면 여기서 규칙 강화 가능
    base = name.rsplit(".", 1)[0]
    return base.strip() if base.strip() else "Unknown"

if run:
    if not files:
        st.error("파일을 업로드하세요.")
        st.stop()
    if len(files) > 10:
        st.error("최대 10개 파일까지만 지원합니다.")
        st.stop()

    model = get_model_name()
    st.info(f"모델: {model} / 동시 처리: {len(files)}")

    results = []
    placeholders = {f.name: st.empty() for f in files}

    def task(file_obj):
        company = _company_from_filename(file_obj.name)
        fulltext = file_obj.read().decode("utf-8", errors="ignore")
        md = generate_oibook(company, fulltext)
        return company, file_obj.name, fulltext, md

    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(task, f): f.name for f in files}
        done_count = 0
        for fut in as_completed(futures):
            fname = futures[fut]
            try:
                company, source_name, fulltext, md = fut.result()
                append_history(company=company, source_name=source_name, fulltext=fulltext, model=model, oibook_md=md)
                results.append((company, source_name, md))
                placeholders[fname].success(f"✅ 완료: {source_name} → {company}")
            except Exception as e:
                placeholders[fname].error(f"❌ 실패: {fname} / {e}")
            done_count += 1
            st.progress(done_count / len(files))

    st.divider()
    st.subheader("결과")
    for company, source_name, md in results:
        with st.expander(f"{company} ({source_name})", expanded=False):
            tab_design, tab_md = st.tabs(["디자인 뷰", "마크다운"])
            with tab_design:
                render_oibook_cards(md, title_override=f"{company} OI Book")
            with tab_md:
                st.markdown(md)
            st.download_button(
                "다운로드(.md)",
                data=md.encode("utf-8"),
                file_name=f"{company}_oi_book.md",
                mime="text/markdown",
            )
