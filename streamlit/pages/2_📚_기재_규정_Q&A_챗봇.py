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
question = st.chat_input("질문을 입력하세요 (예: 행동 특성 및 종합의견에는 어떤 내용을 작성하나요?)")

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
    st.session_state.last_question = question  
    st.session_state.last_answer = answer
    with st.chat_message("assistant"):
        st.markdown("💬 " + answer)

        with st.expander("📄 참조 문서 (Top-3)"):
            for i, doc in enumerate(source_docs):
                # 내용 필터링
                page_text = doc.page_content
                exclusion_phrase = (
                    #목차 때문에 포함되는 부분은 제거하고 참조문서 청크 보여주기
                    "법적근거\n기재요령 \n안내\n목적 등\n인적·\n학적 사항\n출결상황\n수상경력\n자격증 \n취득 및\n국가직무능력\n표준 이수상황\n학교폭력 \n조치상황 \n관리(1·2학년)\n학교폭력 \n조치상황 \n관리(3학년)\n창의적 \n체험활동\n상황\n일상생활\n활동상황\n(특수교육\n기본 교육과정)\n교과학습 \n발달상황\n(1학년)\n교과학습 \n발달상황\n(2·3년)\n독서\n활동상황\n행동특성 및 \n종합의견\n기타 \n사항 등\n참고자료\n"
                )
                if exclusion_phrase in page_text:
                    page_text = page_text.replace(exclusion_phrase, "").strip()

                # 출력
                st.markdown(f"""
                <div style="background-color:#f9f9f9; color:#222; padding:10px; margin:10px 0; border-left:5px solid #bbb;">
                <b>📚 # {i+1}</b><br>
                <b>📁 문서:</b> {doc.metadata.get('source', '알 수 없음')}<br>
                <b>🔍 내용:</b><br>{page_text}
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