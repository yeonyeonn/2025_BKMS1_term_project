import streamlit as st
import sqlite3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from QAchatbot_BE.rag_favorite_db import init_favorites_db, save_favorite, get_favorites, delete_favorite

st.set_page_config(page_title="생기부 문장 생성기", layout="wide")

st.title("생활기록부 작성 도우미")

st.markdown("#### 학생 정보")
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("이름", placeholder="홍길동")
with col2:
    career = st.selectbox("학년",[1, 2, 3])
with col3:
    subject = st.selectbox("반", [1, 2, 3, 4, 5, 6, 7])

st.markdown("#### 작성 요청")
prompt = st.text_area("아래에 작성할 내용을 입력해주세요.", placeholder="예: 000 학생의 동아리 활동을 생활기록부 문장으로 작성해줘.", height=150)

# 문장 생성 실행 버튼
if st.button("📄 생활기록부 문장 생성"):
    if not prompt.strip():
        st.warning("작성 요청란에 내용을 입력해주세요.")
    else:
        # 실제 OpenAI 호출 및 벡터 검색이 들어갈 자리
        # 예시 출력
        st.markdown("---")
        st.subheader("📘 작성 예시")
        st.success("000 학생은 로봇동아리 활동에 적극적으로 참여하며 문제 해결력과 팀워크를 기름.")

        st.subheader("🪄 다른 표현 예시")
        st.info("- 로봇동아리에서 팀 프로젝트를 성실히 수행하며 창의성과 책임감을 보여줌")
        st.info("- 동아리 활동을 통해 협업과 실천 역량을 키움")

        st.subheader("📑 참고한 학생 정보")
        st.code("활동명: 로봇동아리\n역할: 팀 리더\n기간: 2024.03 ~ 2024.11\n활동 내용: 로봇 제작 및 발표 참여")

        st.subheader("📚 참고한 기재 규정")
        st.markdown("""
        - 동아리활동은 참여도, 협력도, 열성도, 특별한 활동 실적 등을 고려하여 실제적인 활동과 역할 위주로 입력한다.\n        - 정규교육과정 내 동아리는 학년 초에 구성하여 학기 말까지 활동한 내용을 모두 기록해야 한다.
        """)

# 즐겨찾기 툴바 형태 사이드 출력
favorites = get_favorites()
selected_fav = st.sidebar.selectbox("⭐ 즐겨찾기한 Q&A", favorites, format_func=lambda row: row[1])

if selected_fav:
    fav_id = selected_fav[0]
    conn = sqlite3.connect("favorites.db")
    c = conn.cursor()
    c.execute("SELECT question, answer FROM favorites WHERE id = ?", (fav_id,))
    q, a = c.fetchone()
    conn.close()

    with st.sidebar.expander("📌 저장된 답변 보기", expanded=False):
        st.markdown(f"**Q. {q}**")
        st.markdown(a)

        if st.button("🗑️ 삭제하기", key=f"delete_{fav_id}"):
            delete_favorite(fav_id)
            st.toast("🗑️ 즐겨찾기가 삭제되었습니다.")
            st.rerun()
