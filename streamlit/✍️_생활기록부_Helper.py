import streamlit as st
from PIL import Image
from pathlib import Path
import os

# 현재 파일 기준 디렉토리 (✍️_생활기록부_Helper.py 기준)
BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "icon_.png"

print("Current working dir:", os.getcwd())
print("Icon absolute path:", ICON_PATH)

st.set_page_config(page_title="생기부 작성 도우미", layout="centered")

# 아이콘 출력
if ICON_PATH.exists():
    st.image(str(ICON_PATH), width=100)
else:
    st.warning(f"아이콘 이미지를 찾을 수 없습니다: {ICON_PATH}")

st.title("생활기록부 Helper")

st.markdown("""
안녕하세요! 👋  
**생활기록부 Helper**는 교사의 생기부 작성 업무를 빠르고, 규정에 맞게 도와주는 **AI 기반 도우미**입니다.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("✍️ 생활기록부 작성 도우미")
    st.markdown("""
    학생의 **활동, 수상, 진로** 등을 바탕으로  
    자연스럽고 규정에 맞는 문장을 자동 생성합니다.
    """)

with col2:
    st.subheader("❓ 기재 규정 Q&A")
    st.markdown("""
    교육부 **기재 요령** 기반  
    어떤 질문이든 규정에 맞게 챗봇이 답변해줍니다.
    """)

st.markdown("---")

st.markdown("""
👈 왼쪽 **사이드바 메뉴**에서 기능을 선택해 시작해보세요!
""")
