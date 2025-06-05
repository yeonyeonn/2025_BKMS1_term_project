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
if "last_failed_sql" not in st.session_state:
    st.session_state.last_failed_sql = ""
if "reasoning_cache" not in st.session_state:
    st.session_state.reasoning_cache = ""

# 메인 처리: 처음 "생활기록부 생성" 버튼 클릭 시
if st.button("생활기록부 생성"):
    if user_query.strip():
        st.session_state.life_record_candidates = []
        st.session_state.student_data = None
        st.session_state.last_failed_sql = ""
        st.session_state.user_query_cache = user_query

        with st.spinner("자연어를 SQL로 변환 중..."):
            result = nlTosql(user_query)

        if not result or not isinstance(result, dict):
            st.error("❌ SQL 문 생성에 실패했습니다. 질문을 다시 입력해 주세요.")
        else:
            reasoning = result.get("chain_of_thought_reasoning", "")
            sql_query = result.get("SQL", "")

            st.session_state.reasoning_cache = reasoning
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

                            st.session_state.student_data = data
                            st.success(f"✅ {len(data)}건의 데이터를 조회했습니다.")
                            st.json(data)

                    except Exception as e:
                        st.session_state.last_failed_sql = sql_query
                        st.error(f"❗ 쿼리 실행 실패: {e}")

# SQL 수정 후 재실행 UI
if st.session_state.last_failed_sql:
    st.markdown("### ⚠️ SQL 실행 실패 - 직접 수정해서 다시 시도해보세요.")
    modified_sql = st.text_area("수정된 SQL 쿼리 입력:", value=st.session_state.last_failed_sql)

    if st.button("쿼리 다시 실행"):
        with st.spinner("수정된 SQL 실행 중..."):
            try:
                cursor.execute(modified_sql)
                rows = cursor.fetchall()

                if not rows:
                    st.warning("🔍 해당 조건에 맞는 데이터가 없습니다.")
                else:
                    columns = [desc[0] for desc in cursor.description]
                    data = [dict(zip(columns, row)) for row in rows]

                    st.session_state.student_data = data
                    st.session_state.last_failed_sql = ""  # 실패 기록 초기화
                    st.success(f"✅ {len(data)}건의 데이터를 조회했습니다.")
                    st.json(data)

            except Exception as e:
                st.error(f"❗ 수정된 쿼리 실행 실패: {e}")

# 후보가 없고, 데이터가 있을 경우에만 LLM 문장 생성
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

# 생성된 문장 선택 UI
if st.session_state.life_record_candidates:
    candidates = st.session_state.life_record_candidates

    # ✅ 항상 데이터 표시
    if st.session_state.student_data:
        st.markdown("### 📊 조회된 학생 데이터")
        st.json(st.session_state.student_data)

    selected = st.radio(
        "📄 생성된 생활기록부 후보 중 하나를 선택하세요:",
        options=candidates,
        format_func=lambda x: x[:80] + "..." if len(x) > 80 else x,
        key="selected_life_record"
    )

    st.subheader("✅ 선택된 생활기록부 문장")
    st.write(selected)

