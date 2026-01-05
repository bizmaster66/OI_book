import streamlit as st
import datetime as dt
from src.ui.styles import inject_global_styles
from src.ui.oibook_view import render_oibook_cards
from src.store.history_store import load_history

inject_global_styles()
st.title("History: 생성 이력")

items = load_history(limit=200)

if not items:
    st.info("아직 생성된 이력이 없습니다.")
    st.stop()

st.caption(f"총 {len(items)}건 (최신순)")

for it in items:
    ts = dt.datetime.fromtimestamp(it.ts).strftime("%Y-%m-%d %H:%M:%S")
    header = f"{it.company} | {it.source_name} | {ts} | model={it.model}"
    with st.expander(header, expanded=False):
        tab_design, tab_md = st.tabs(["디자인 뷰", "마크다운"])
        with tab_design:
            render_oibook_cards(it.oibook_md, title_override=f"{it.company} OI Book")
        with tab_md:
            st.markdown(it.oibook_md)
        st.download_button(
            "마크다운 다운로드(.md)",
            data=it.oibook_md.encode("utf-8"),
            file_name=f"{it.company}_oi_book_{it.fulltext_sha}.md",
            mime="text/markdown",
        )
