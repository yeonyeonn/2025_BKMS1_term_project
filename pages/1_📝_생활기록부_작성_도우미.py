import streamlit as st

st.set_page_config(page_title="생기부 문장 생성기", layout="wide")

st.title("생활기록부 작성 도우미")

st.markdown("#### 학생 정보 입력")
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("이름", placeholder="홍길동")
with col2:
    career = st.text_input("진로희망", placeholder="의사")
with col3:
    subject = st.selectbox("분야 선택", ["동아리", "대회", "봉사", "독서", "국어", "수학", "과학", "사회", "영어", "기타"])

row1, row2 = st.columns([6, 1])
with row1:
    st.markdown("#### 활동 입력")
with row2:
    if st.button("🗑️ 전체 초기화"):
        st.session_state.activities = [""]
        st.session_state.generated = []

if "activities" not in st.session_state:
    st.session_state.activities = [""]

new_activities = []
for i, activity in enumerate(st.session_state.activities):
    new = st.text_input(f"활동 {i+1}", value=activity, key=f"activity_{i}", placeholder="예: 탐구 보고서를 작성함")
    new_activities.append(new)

if st.button("➕ 활동 추가"):
    st.session_state.activities.append("")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("📄 문장 생성"):
    st.session_state.generated = [f"{a} → 예시 문장입니다." for a in new_activities if a.strip() != ""]

if "generated" in st.session_state and st.session_state.generated:
    st.markdown("#### 결과 미리보기")
    for idx, sentence in enumerate(st.session_state.generated):
        st.success(f"문장 {idx+1}: {sentence}")
    st.markdown("---")
    st.markdown("**📌 단락 예시:**")
    st.markdown("""
    <div style='padding: 1rem; background-color: #eaf4ff; border-radius: 0.5rem; font-size: 1.1rem;'>
        학생은 다양한 활동에 적극적으로 참여하며 자기주도성과 협업능력을 기름. (예시)
    </div>
    """, unsafe_allow_html=True)

# 즐겨찾기 툴바 형태 사이드 출력
with st.sidebar:
    st.markdown("### ⭐ 즐겨찾기한 기재 요령")
    if "favorites" in st.session_state and st.session_state.favorites:
        for i, fav in enumerate(st.session_state.favorites):
            st.markdown(f"- {fav}")
    else:
        st.info("즐겨찾기한 항목이 없습니다. Q&A 페이지에서 추가해보세요.")