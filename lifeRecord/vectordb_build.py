import json
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

# === 경로 설정 ===
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SCHEMA_FILE = DATA_DIR / "lifeRecordSchema.json"
FEWSHOT_FILE = DATA_DIR / "fewshot.jsonl"
API_KEY_FILE = DATA_DIR / "api_key.txt"
DB_PATH = BASE_DIR / "vectordb"

# === OpenAI API 키 로딩 ===
def load_api_key(api_key_path):
    with open(api_key_path, "r", encoding="utf-8") as f:
        return f.read().strip()

OPENAI_API_KEY = load_api_key(API_KEY_FILE)

# === 1. schema (column description) 저장 ===
def save_column_descriptions(schema_file: str):
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_data = json.load(f)

    documents, metadatas, ids = [], [], []

    for table in schema_data:
        table_name = table["table"]
        for col in table["column"]:
            col_name = col["column_name"]
            description = col.get("description", "").lstrip("#").strip()
            document = f"column_name: {col_name}\n{description}"
            documents.append(document)
            metadatas.append({
                "table": table_name,
                "column": col_name
            })
            ids.append(f"col-{table_name}-{col_name}")

    client = chromadb.PersistentClient(path=str(DB_PATH))
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-3-small"
    )

    collection = client.get_or_create_collection("column_description", embedding_function=openai_ef)

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print("✅ Column descriptions saved to ChromaDB!")


# === 2. few-shot 예시 저장 ===
def save_fewshot_examples(fewshot_file: str):
    records = []
    with open(fewshot_file, 'r', encoding='utf-8') as f:
        for line in f:
            records.append(json.loads(line))

    df = pd.DataFrame(records)

    client = chromadb.PersistentClient(path=str(DB_PATH))
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-3-small"
    )

    collection = client.get_or_create_collection("fewshot", embedding_function=openai_ef)

    documents = df["question"].tolist()
    metadatas = df[["evidence", "question", "SQL"]].to_dict(orient="records")
    ids = ["few-shot-" + str(qid) for qid in df["question_id"]]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print("✅ Few-shot examples saved to ChromaDB!")


# === 실행 ===
if __name__ == "__main__":
    save_column_descriptions(SCHEMA_FILE)
    save_fewshot_examples(FEWSHOT_FILE)
