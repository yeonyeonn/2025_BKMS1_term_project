import streamlit as st
import sqlite3
import os
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import json
from pathlib import Path
from QAchatbot_BE.rag_favorite_db import init_favorites_db, save_favorite, get_favorites, delete_favorite



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
st.title("생활기록부 작성 도우미")

user_query = st.text_input("생활기록부에 작성하고자 하는 내용을 자연어로 입력하세요:")

# 세션 상태 초기화
if "life_record_candidates" not in st.session_state:
    st.session_state.life_record_candidates = {}  # student_id -> list of 3 candidates
if "student_data" not in st.session_state:
    st.session_state.student_data = None
if "user_query_cache" not in st.session_state:
    st.session_state.user_query_cache = ""
if "last_failed_sql" not in st.session_state:
    st.session_state.last_failed_sql = ""
if "reasoning_cache" not in st.session_state:
    st.session_state.reasoning_cache = ""

# "생활기록부 생성" 버튼 클릭 시 처리
if st.button("생활기록부 생성"):
    if user_query.strip():
        st.session_state.life_record_candidates = {}
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
            st.markdown("---")
            st.markdown("#### 🧠 AI 도우미의 사고 과정(Chain of Thought Reasoning)")
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

                    except Exception as e:
                        st.session_state.last_failed_sql = sql_query
                        st.error(f"❗ 쿼리 실행 실패: {e}")

# SQL 수정 후 재실행 UI
if st.session_state.last_failed_sql:
    st.markdown("#### ⚠️ SQL 실행 실패 - 직접 수정해서 다시 시도해보세요.")
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
                    st.session_state.last_failed_sql = ""
                    st.success(f"✅ {len(data)}건의 데이터를 조회했습니다.")

            except Exception as e:
                st.error(f"❗ 수정된 쿼리 실행 실패: {e}")

# ✅ 항상 학생 데이터 표시

# 1. 조회된 원본 데이터 출력
#if st.session_state.get("student_data"):
#    st.markdown("### 📊 조회된 데이터")
#    st.markdown(f"- 총 **{len(st.session_state.student_data)}개**의 데이터가 조회되었습니다.")

# 2. 학생 단위로 동아리 활동 병합
grouped_data = {}
if st.session_state.get("student_data"):
    for entry in st.session_state.student_data:
        student_id = entry.get("student_id")
        student_name = entry.get("student_name")
        club_name = entry.get("club_name") or "기타"
        club_desc = entry.get("club_description") or ""
        activity_desc = entry.get("activity_description") or ""
        activity_type = entry.get("activity_type")

        if student_id not in grouped_data:
            grouped_data[student_id] = {
                "student_id": student_id,
                "student_name": student_name,
                "clubs": {},  # 동아리명 기준으로 활동 묶음
                "activity_type": activity_type,  # 필요하면 이걸 리스트로 바꿀 수도 있음
            }

        # 동아리별로 활동 병합
        if club_name not in grouped_data[student_id]["clubs"]:
            grouped_data[student_id]["clubs"][club_name] = {
                "club_description": club_desc,
                "activities": []
            }

        if activity_desc and activity_desc not in grouped_data[student_id]["clubs"][club_name]["activities"]:
            grouped_data[student_id]["clubs"][club_name]["activities"].append(activity_desc)

    # student_id 기준으로 리스트 변환, 동아리별 활동도 문자열로 병합
    merged_student_data = []
    for student_info in grouped_data.values():
        clubs_merged = []
        for club_name, club_info in student_info["clubs"].items():
            activities_text = " / ".join(club_info["activities"])
            clubs_merged.append({
                "club_name": club_name,
                "club_description": club_info["club_description"],
                "activities": activities_text
            })

        merged_student_data.append({
            "student_id": student_info["student_id"],
            "student_name": student_info["student_name"],
            "activity_type": student_info["activity_type"],
            "clubs": clubs_merged
        })

    # 병합된 데이터 보기 (옵션)
    st.markdown("### 🧾 학생별 활동 데이터")
    st.success(f"총 **{len(merged_student_data)}명**의 학생 데이터가 병합되어 조회되었습니다.")
    st.json(merged_student_data)
    # df = pd.DataFrame(merged_student_data)  # 병합된 데이터를 데이터프레임으로 변환
    # st.dataframe(df, use_container_width=True)

    # 3. 후보 생성: 학생 단위로 3개씩 생성, 동아리별 묶음 같이 전달
    if (
        merged_student_data
        and not st.session_state.life_record_candidates
        and st.session_state.user_query_cache
    ):
        with st.spinner("LLM으로 생활기록부 문장 생성 중..."):
            reference = json.dumps(merged_student_data, ensure_ascii=False)
            query_text = st.session_state.user_query_cache

            for student_info in merged_student_data:
                student_id = student_info.get("student_name") or student_info.get("student_id") or str(student_info)
                key = f"{student_id}"

                st.session_state.life_record_candidates[key] = [
                    generate_life_record(student_info, reference, query_text)
                    for _ in range(3)
                ]

    # 4. 후보 문장 선택 UI
    if st.session_state.life_record_candidates:
        st.markdown("### ✨ 학생별 생활기록부 문장 후보 선택")

        for idx, student_info in enumerate(merged_student_data):
            student_id = student_info.get("student_name") or student_info.get("student_id") or str(idx)
            unique_key = f"{student_id}_{idx}"  # 유일한 key 생성

            options = st.session_state.life_record_candidates.get(f"{student_id}", [])

            # ✅ 학생 구역 헤더 강조 (HTML 사용 가능)
            st.markdown(
                f"""
                <div style='margin-top: 2em; margin-bottom: 0.5em; padding: 0.5em; background-color: #f0f2f6; border-left: 5px solid #4CAF50;'>
                    <h4 style='margin: 0; color: black;'>  <b>{student_info.get("student_name", "이름 없음")}</b> ({student_info.get("student_id", "")})</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            selected = st.radio(
                f"**생활기록부 문장 선택**",
                options=options,
                format_func=lambda x: x[:80] + "..." if len(x) > 80 else x,
                key=f"selected_{unique_key}"
            )

            st.markdown("---")
            st.write("✅ 선택된 문장:")
            # st.write(selected)
            st.markdown(
            f"<div style='background-color:#e5f8e3;padding:15px;border-radius:10px;border:2px;font-size:16px;color:black;'>{selected}</div>",
            unsafe_allow_html=True
        )


# 즐겨찾기
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
        st.markdown(f"**A.** {a}")

        if st.button("🗑️ 삭제하기", key=f"delete_{fav_id}"):
            delete_favorite(fav_id)
            st.toast("🗑️ 즐겨찾기가 삭제되었습니다.")
            st.rerun()