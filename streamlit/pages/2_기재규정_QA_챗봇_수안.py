import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from QAchatbot_BE.rag_module import load_rag_chatbot


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


        # 즐겨찾기 버튼
        if st.button("⭐ 이 답변 즐겨찾기", key=f"fav_{len(st.session_state.messages)}"):
            if answer not in st.session_state.favorites:
                st.session_state.favorites.append(answer)
                st.success("즐겨찾기에 추가되었습니다!")
            else:
                st.info("이미 추가된 항목입니다.")

# 즐겨찾기 표시
with st.sidebar:
    st.markdown("### ⭐ 즐겨찾기한 Q&A")
    if st.session_state.favorites:
        for fav in st.session_state.favorites:
            st.markdown(f"- {fav}")
    else:
        st.info("즐겨찾기가 없습니다.")
