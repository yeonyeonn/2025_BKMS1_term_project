import streamlit as st

st.set_page_config(page_title="생기부 작성 도우미", layout="centered")

st.title("📘 생활기록부 Plus")
st.markdown("""
이 앱은 GPT 및 RAG 기반으로 교사의 생기부 작성을 도와주는 도구입니다.

왼쪽 사이드바에서 다음 기능을 이용해보세요:
- **생활기록부 작성 도우미**: 학생 활동을 바탕으로 자연스러운 문장 생성
- **기재 규정 Q&A**: 생기부 기재 요령을 챗봇에게 질문
""")

