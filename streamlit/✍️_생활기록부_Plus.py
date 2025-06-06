import streamlit as st
from PIL import Image

st.set_page_config(page_title="생기부 작성 도우미", layout="centered")

# 헤더 이미지나 아이콘 (선택사항)
st.image("https://i.namu.wiki/i/qY_em2Rh2-VybNYhMhX0AcVYfVqik1Cc7hCAzPAgDrDTl12Ss8_-ChSmXIRx7v0qKq_sze3ZEhbQeqQWf7xXSmhBcAs4rpdPPAYhvs2uuEk.svg", width=100)

# 타이틀
st.title("생활기록부 Plus")

# 간단한 환영 메시지
st.markdown("""
안녕하세요! 👋  
**생활기록부 Plus**는 교사의 생기부 작성 업무를 빠르고, 규정에 맞게 도와주는 **AI 기반 도우미**입니다.
""")

# 구분선
st.markdown("---")

# 기능 소개 (카드 형태)
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

# 구분선
st.markdown("---")

# 안내 문구
st.markdown("""
👈 왼쪽 **사이드바 메뉴**에서 기능을 선택해 시작해보세요!
""")
