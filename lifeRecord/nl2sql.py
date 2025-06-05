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

    fewshots_text = get_relevant_fewshots(user_question, top_k=3)

    prompt_template = """   
                        당신은 현재 생활기록부를 작성 중인 교사를 도와 필요한 데이터를 찾는 일을 수행하고 있습니다.
                        생활기록부(학생생활기록부)는 대한민국 초·중·고 학생들의 학교 생활 전반을 공식적으로 기록하는 문서로, 
                        교사들이 작성하며 대학 입시나 취업 시 중요한 평가 자료로 활용됩니다.
                        학생의 활동, 교과 성적, 수상, 봉사 등 모든 정보가 빠짐없이 잘 반영되도록 적절한 데이터를 추출하는 것이 매우 중요합니다.

                        아래에 데이터베이스 스키마와 사용자의 질문 혹은 명령이 주어집니다.
                        스키마를 꼼꼼히 분석하여 사용자의 의도를 정확히 이해한 후, 생활기록부 작성에 필요한 데이터를 찾기 위한 최적의 SQLite 쿼리를 작성하세요.
                        쿼리 작성 전, 사용자가 요구하는 조건(예: 학년, 학기, 활동 유형, 동아리명, 과목명 등)을 단계별로 분석하며 사고 과정을 서술해 주세요.

                        특히, 다음 사항을 주의 깊게 고려하세요:
                        - 날짜(정확한 날짜, 연도, 학기): 연도와 학기로 질의가 들어온 경우 범위를 통해 해당 날짜가 그 범위에 들어가는지 확인해야합니다.
                            활동 날짜의 경우 "activity_date"로 확인가능합니다.
                            ex) 2024년 1학기는 날짜로 2024-03-01에서 2024-07-31 사이의 값입니다.
                        - 활동 유형 (예: 동아리 활동, 자율 활동, 진로 활동, 특기 적성)
                        - 특정 동아리명 (예: 피타고라스)
                        - 학생 개인 혹은 그룹 대상 여부

                        아래는 데이터베이스 스키마입니다:
                        {DATABASE_SCHEMA}

                        아래는 예시 질문 및 쿼리입니다:
                        {FEWSHOTS}

                        사용자 질문 혹은 명령:
                        {QUESTION}

                        힌트:
                        {HINT}

                        최종 결과는 다음 JSON 형태로 출력하세요:

                        {{
                        "chain_of_thought_reasoning": "당신이 최종 SQL 쿼리를 작성하기 위해 분석한 단계별 사고 과정",
                        "SQL": "최종 작성한 SQLite 쿼리문"
                        }}

                        질문에 맞는 정확하고 완전한 쿼리를 단계별로 신중하게 작성해 주세요.
                        """

    prompt = prompt_template.format(
        DATABASE_SCHEMA=schema_info,
        QUESTION=user_question,
        HINT="",  # 필요시 힌트 추가 가능
        FEWSHOTS="",
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

        output_lines.append(f"테이블명: {table_name}")

        for col in table_columns:
            col_name = col["column_name"]
            is_pk = col["PK"] == 1
            fk = col["FK"]
            desc = col.get("description", None)

            if is_pk:
                output_lines.append(f"- 컬럼 (PK): {col_name}")
            elif fk:
                output_lines.append(f"- 컬럼 (FK): {col_name}")
            else:
                output_lines.append(f"- 컬럼: {col_name}")

            if include_descriptions and desc:
                cleaned = desc.strip().lstrip("#").strip()
                output_lines.append(f"  - 설명: {cleaned}")

        output_lines.append("")

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