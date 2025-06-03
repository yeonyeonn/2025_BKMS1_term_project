import streamlit as st
import sys
import os
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from QAchatbot_BE.rag_module import load_rag_chatbot
from QAchatbot_BE.rag_favorite_db import init_favorites_db, save_favorite, get_favorites, delete_favorite
init_favorites_db()


st.set_page_config(page_title="📚 기재 규정 Q&A")

st.title("생활기록부 기재 규정 Q&A")
st.markdown("기재 요령에 대해 궁금한 점을 입력해보세요. 교육부 문서를 기반으로 답변합니다.")

# QA 체인 초기화
if "qa_chain" not in st.session_state:
    with st.spinner("🔧 RAG QA 시스템 로드 중..."):
        st.session_state.qa_chain = load_rag_chatbot(persist_path="../vectordb")
        st.session_state.messages = []  # 대화 기록 초기화
        st.session_state.favorites = []

# 이전 대화 출력
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)

# 새 질문 입력 (채팅 스타일)
question = st.chat_input("질문을 입력하세요 (예: 창의적 체험활동 항목은 어떻게 쓰나요?)")

if question:
    # 사용자 질문 출력
    st.session_state.messages.append(("user", question))
    with st.chat_message("user"):
        st.markdown(question)

    # GPT 답변 생성
    with st.spinner("답변 생성 중..."):
        result = st.session_state.qa_chain(question)
        answer = result["answer"]
        print("answer front!!!!")
        print(answer)
        source_docs = result["source_documents"]
        print("source front!!!!")
        print(source_docs)

    # GPT 답변 출력
    st.session_state.messages.append(("assistant", answer))
    st.session_state.last_question = question  # 다연 추가
    st.session_state.last_answer = answer
    with st.chat_message("assistant"):
        st.markdown("💬 " + answer)

        with st.expander("📄 참조 문서 (Top-3)"):
            for i, doc in enumerate(source_docs):
                st.markdown(f"""
                <div style="background-color:#f9f9f9; color:#222; padding:10px; margin:10px 0; border-left:5px solid #bbb;">
                <b>📚 청크 ID:</b> chunk_{i}<br>
                <b>📁 문서:</b> {doc.metadata.get('source', '알 수 없음')}<br>
                <b>🔍 내용:</b><br>{doc.page_content}
                </div>
                """, unsafe_allow_html=True)


## 즐겨찾기 구현
if st.session_state.get("last_answer"):
    if st.button("⭐ 이 답변 즐겨찾기"):
        success = save_favorite(
            st.session_state.last_question,
            st.session_state.last_answer
        )
        if success:
            st.session_state.just_saved = True
        else:
            st.session_state.already_saved = True
        st.rerun()

# 상단에 메시지 띄우기
if st.session_state.get("just_saved"):
    st.success("✅ 즐겨찾기에 저장되었습니다.")
    st.session_state.just_saved = False

if st.session_state.get("already_saved"):
    st.info("⚠️ 이미 즐겨찾기에 추가된 답변입니다.")
    st.session_state.already_saved = False



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