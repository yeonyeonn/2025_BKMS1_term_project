import streamlit as st
import sqlite3
import sys
import json
from pathlib import Path

# 경로 설정
base_path = Path(__file__).resolve().parents[2] / "lifeRecord"
sys.path.append(str(base_path))

# 모듈 임포트
from nl2sql import nlTosql
from generateText import generate_life_record

# DB 연결
db_path = base_path / "DB" / "student_record.sqlite"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Streamlit UI
st.title("생활기록부 생성기")

user_query = st.text_input("학생 정보에 대해 알고 싶은 내용을 자연어로 입력하세요:")

# 세션 상태 초기화
if "life_record_candidates" not in st.session_state:
    st.session_state.life_record_candidates = []
if "student_data" not in st.session_state:
    st.session_state.student_data = None
if "user_query_cache" not in st.session_state:
    st.session_state.user_query_cache = ""

if st.button("생활기록부 생성"):
    if user_query.strip():
        st.session_state.life_record_candidates = []  # 새 쿼리일 경우 후보 초기화
        st.session_state.user_query_cache = user_query

        with st.spinner("자연어를 SQL로 변환 중..."):
            result = nlTosql(user_query)

        if not result or not isinstance(result, dict):
            st.error("❌ SQL 문 생성에 실패했습니다. 질문을 다시 입력해 주세요.")
        else:
            reasoning = result.get("chain_of_thought_reasoning", "")
            sql_query = result.get("SQL", "")

            # 🧠 사고 과정 출력
            st.markdown("### 🧠 사고 과정 (Chain of Thought Reasoning)")
            st.write(reasoning)

            if not sql_query:
                st.error("❌ SQL 쿼리가 생성되지 않았습니다.")
            else:
                with st.spinner("DB에서 데이터 조회 중..."):
                    try:
                        cursor.execute(sql_query)
                        rows = cursor.fetchall()

                        if not rows:
                            st.warning("🔍 해당 조건에 맞는 데이터가 없습니다.")
                        else:
                            columns = [desc[0] for desc in cursor.description]
                            data = [dict(zip(columns, row)) for row in rows]

                            st.session_state.student_data = data  # 저장
                            st.success(f"✅ {len(data)}건의 데이터를 조회했습니다.")
                            st.json(data)

                    except Exception as e:
                        st.error(f"❗ 쿼리 실행 실패: {e}")
    else:
        st.warning("질문을 먼저 입력해 주세요.")

# 후보가 없고, 데이터가 있을 경우에만 생성
if (
    st.session_state.student_data
    and not st.session_state.life_record_candidates
    and st.session_state.user_query_cache
):
    with st.spinner("LLM으로 생활기록부 문장 생성 중..."):
        student_info = st.session_state.student_data[0]
        reference = json.dumps(st.session_state.student_data, ensure_ascii=False)
        query_text = st.session_state.user_query_cache

        st.session_state.life_record_candidates = [
            generate_life_record(student_info, reference, query_text)
            for _ in range(3)
        ]

# 후보가 있을 경우 라디오 버튼 표시
if st.session_state.life_record_candidates:
    candidates = st.session_state.life_record_candidates

    selected = st.radio(
        "📄 생성된 생활기록부 후보 중 하나를 선택하세요:",
        options=candidates,
        format_func=lambda x: x[:80] + "..." if len(x) > 80 else x,
        key="selected_life_record"
    )

    st.subheader("✅ 선택된 생활기록부 문장")
    st.write(selected)

