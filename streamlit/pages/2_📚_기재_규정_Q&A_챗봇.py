import streamlit as st

st.set_page_config(page_title="📚 기재 규정 Q&A")

st.title("생활기록부 기재 규정 Q&A")

st.markdown("기재 요령에 대해 궁금한 점을 입력해보세요. 교육부에서 작성한 2025학년도 고등학교 학교생활기록부 기재요령에 기반하여 답변합니다.")

question = st.text_input("질문 입력", placeholder="예: 세특 항목은 몇 자까지 작성 가능한가요?")

if st.button("질문하기"):
    st.markdown("---")
    st.write("💬 **답변:**")
    answer = "세특 항목은 1500byte 또는 500자까지 작성할 수 있습니다. (예시 답변)"
    st.success(answer)
    st.caption("※ 실제 RAG 연결 시 실제 규정 문서 기반 응답 제공")

    if "favorites" not in st.session_state:
        st.session_state.favorites = []

    if st.button("⭐ 이 답변 즐겨찾기"):
        if answer not in st.session_state.favorites:
            st.session_state.favorites.append(answer)
            st.success("즐겨찾기에 추가되었습니다!")
        else:
            st.info("이미 즐겨찾기에 추가된 항목입니다.")

# 즐겨찾기 툴바 형태 사이드 출력
with st.sidebar:
    st.markdown("### ⭐ 즐겨찾기한 기재 요령")
    if "favorites" in st.session_state and st.session_state.favorites:
        for i, fav in enumerate(st.session_state.favorites):
            st.markdown(f"- {fav}")
    else:
        st.info("즐겨찾기한 항목이 없습니다. Q&A 페이지에서 추가해보세요.")