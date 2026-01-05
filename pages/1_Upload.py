import streamlit as st

st.set_page_config(page_title="OI BOOK - Upload", layout="wide")
st.title("1) 업로드")

uploaded = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

if uploaded:
    st.success(f"업로드 완료: {uploaded.name}")
    st.info("다음 단계: 왼쪽 메뉴에서 '2) 텍스트 추출'로 이동하세요.")
else:
    st.caption("※ 현재는 UI 뼈대 단계입니다. 다음 단계에서 업로드 파일을 세션/스토리지로 전달합니다.")
