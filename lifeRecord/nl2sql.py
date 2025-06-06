# lifeRecord/NL2SQL.py
import openai
from pathlib import Path
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os
import json
import pandas as pd
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "vectordb"

SCHEMA_FILE = DATA_DIR / "lifeRecordSchema.json"
FEWSHOT_FILE = DATA_DIR / "fewshot.jsonl"
API_KEY_FILE = DATA_DIR / "api_key.txt"

def load_api_key(api_key_path):
    with open(api_key_path, "r", encoding="utf-8") as f:
        return f.read().strip()

OPENAI_API_KEY = load_api_key(API_KEY_FILE)

def nlTosql(user_question):
    llm = openai.OpenAI(api_key=OPENAI_API_KEY)

    relevant_columns = find_relevant_columns(user_question, top_k=5)

    schema_info = generate_filtered_schema(
        input_file=SCHEMA_FILE,
        used_columns=relevant_columns,
        include_descriptions=True
    )

    fewshots_text = get_relevant_fewshots(user_question, top_k=2)

    prompt_template =   """
                        당신은 대한민국 학생생활기록부를 작성하는 교사를 도와, 필요한 데이터를 데이터베이스에서 정확히 추출하는 역할을 맡고 있습니다.

                        생활기록부는 초·중·고 학생들의 학교생활 전반을 공식적으로 기록하는 문서로, 대학 입시 및 취업에 매우 중요한 평가 자료입니다.
                        따라서 교사의 질문이나 명령을 정확히 분석하여, 적절한 SQLite 쿼리를 생성해야 합니다.

                        ---

                        **당신의 작업 순서:**
                        1. 사용자 질문 또는 명령을 분석합니다.
                        2. 필요한 조건(학년, 학기, 활동 유형, 동아리명, 과목명 등)을 단계별로 추출하고 논리적으로 정리합니다.
                        3. 정확하고 완전한 SQLite 쿼리를 작성합니다.

                        ---

                        **쿼리 작성 시 유의사항:**
                        - 반드시 쿼리 결과에 학생 정보(`student.student_id`, `student.student_name`)를 포함해야 합니다.
                        - 활동 유형을 포함하고 그 유형에 따라 추가 정보 포함:
                            - 활동 유형이 '동아리활동'인 경우 `club_name` 및 `club_description` 반드시 포함해야 합니다.
                            - 이 때 activity에서 club으로의 접근은 Foreign key인 club_id를 활용합니다.
                        - `activity_description`(활동 설명)은 항상 포함해야 합니다.
                        - 질문에 특정 동아리명(예: '피타고라스')이 포함된 경우, 해당 동아리에 한정해야 합니다.
                        - 활동의 대상이 개인인지 그룹인지도 고려해야 합니다.
                        - 날짜 조건이 있는 경우:
                            - `activity_date`를 기준으로 필터링.
                            - 예) 2024년 1학기 → `2024-03-01` ~ `2024-07-31` 범위로 간주.

                        ---

                        **데이터베이스 스키마:**
                        {DATABASE_SCHEMA}

                        ---

                        **예시 질문 및 쿼리:**
                        {FEWSHOTS}

                        ---

                        **사용자 질문 또는 명령:**
                        {QUESTION}

                        {HINT}

                        ---

                        **최종 출력 형식 (JSON):**
                        {{
                        "chain_of_thought_reasoning": "최종 SQL 쿼리를 만들기 위한 당신의 단계별 사고 과정",
                        "SQL": "작성한 최종 SQLite 쿼리"
                        }}

                        위 규칙에 따라 신중하게 생각을 전개하고 정확한 SQL을 작성하세요.
                        """


    prompt = prompt_template.format(
        DATABASE_SCHEMA=schema_info,
        QUESTION=user_question,
        HINT="",  # 필요시 힌트 추가 가능
        FEWSHOTS=fewshots_text,
    )

    response = llm.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    generated_text = response.choices[0].message.content
    print("LLM 응답:\n", generated_text)

    import re

    try:
        # JSON 객체 블록 추출 시도
        match = re.search(r"\{.*\}", generated_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            generated_dict = json.loads(json_str)
            return generated_dict
        else:
            print("JSON 형식 블록을 찾을 수 없습니다")
            return None
    except json.JSONDecodeError as e:
        print("JSON 파싱 실패:", e)
        print("파싱 시도한 문자열:\n", json_str)
        return None



def find_relevant_columns(query, top_k=7):
    client = chromadb.PersistentClient(path=str(DB_PATH))

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-3-small"
    )

    collection = client.get_or_create_collection("column_description", embedding_function=openai_ef)

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    print(f"\n🔍 사용자 질문과 관련된 상위 {top_k}개 컬럼:")

    best_score = 100000
    for doc, meta, score in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        print(f"# 테이블: {meta['table']}, 컬럼: {meta['column']}")
        print(f"# 설명: {doc.splitlines()[1]}")
        print(f"# 유사도 점수: {score:.4f}\n")
        if score < best_score:
            best_score = score

    print(f"최고 점수: {best_score:.4f}")

    return results['metadatas'][0]


def generate_filtered_schema(input_file, used_columns=None, include_descriptions=True):
    with open(input_file, "r", encoding="utf-8") as f:
        tables = json.load(f)

    output_lines = []

    if used_columns:
        used_set = set((item["table"], item["column"]) for item in used_columns)
    else:
        used_set = None

    for table in tables:
        table_name = table["table"]

        if used_set:
            table_columns = [col for col in table["column"] if (table_name, col["column_name"]) in used_set]
            if not table_columns:
                continue
        else:
            table_columns = table["column"]

        output_lines.append(f"\n📘 테이블: {table_name}")

        for col in table_columns:
            col_name = col["column_name"]
            is_pk = col["PK"] == 1
            fk = col.get("FK")  # ← 여기만 방어적으로 수정
            desc = col.get("description", None)

            # 컬럼 정보 라인 구성
            col_line = f" - 컬럼: {col_name}"
            if is_pk:
                col_line += " (PK)"
            elif isinstance(fk, dict):  # FK일 때만 명확하게 표시
                ref_table = fk.get("table")
                ref_column = fk.get("column")
                col_line += f" (FK → {ref_table}.{ref_column})"

            output_lines.append(col_line)

            # 설명 포함
            if include_descriptions and desc:
                cleaned = desc.strip().lstrip("#").strip()
                output_lines.append(f"    • 설명: {cleaned}")

        output_lines.append("")  # 테이블 끝 간격

    return "\n".join(output_lines)




def get_relevant_fewshots(user_question, top_k=3):
    client = chromadb.PersistentClient(path=str(DB_PATH))
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-3-small"
    )
    collection = client.get_or_create_collection("fewshot", embedding_function=openai_ef)

    results = collection.query(
        query_texts=[user_question],
        n_results=top_k
    )

    fewshot_blocks = []
    for idx, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0]), 1):
        block = f"""### 예제 {idx}
                        질문: {meta['question']}
                        근거: {meta['evidence']}
                        SQL:
                        {meta['SQL']}"""
        fewshot_blocks.append(block)

    return "\n\n".join(fewshot_blocks)

#if __name__ == "__main__":
#    question = "2024년 1학기 수학 동아리인 피타고라스에 활동한 이원정 학생의 활동을 바탕으로 생기부를 작성해줘"
#    result = nlTosql(question)