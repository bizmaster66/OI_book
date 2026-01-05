from __future__ import annotations

import html
from typing import List, Tuple, Optional

import streamlit as st
from markdown import markdown as md_to_html


def split_oibook_sections(md_text: str) -> Tuple[Optional[str], List[Tuple[str, str]]]:
    title: Optional[str] = None
    sections: List[Tuple[str, str]] = []
    current_title: Optional[str] = None
    current_lines: List[str] = []

    for line in md_text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip() or title
            continue
        if line.startswith("## "):
            if current_title is not None:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line[3:].strip()
            current_lines = []
            continue
        if current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        sections.append((current_title, "\n".join(current_lines).strip()))

    return title, sections


def render_oibook_cards(md_text: str, *, title_override: Optional[str] = None) -> None:
    title, sections = split_oibook_sections(md_text)
    display_title = title_override or title or "OI Book"

    st.markdown(
        f"""
<div class="oi-card">
  <div class="oi-card-title">{html.escape(display_title)}</div>
  <div class="oi-muted">생성된 마크다운을 섹션 카드로 표시합니다.</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if not sections:
        st.info("섹션을 찾지 못했습니다. 원문 마크다운을 확인하세요.")
        st.markdown(md_text)
        return

    for section_title, section_body in sections:
        body = section_body.strip() or "_내용 없음_"
        body_html = md_to_html(body, extensions=["extra"])
        st.markdown(
            f'<div class="oi-section"><h3>{html.escape(section_title)}</h3>{body_html}</div>',
            unsafe_allow_html=True,
        )
