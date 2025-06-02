# build_vector_db.py

from langchain_community.document_loaders import PyMuPDFLoader  
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma            
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from tqdm import tqdm                
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def build_vector_db(pdf_path: str, persist_path: str):
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY가 .env 파일에 존재하지 않습니다.")
    
    os.makedirs(persist_path, exist_ok=True)


    print(f"*******PDF 불러오는 중... 경로: {pdf_path}")
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    print("******* 텍스트 청크 분할 중...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)
    print(f"******* 총 {len(documents)}쪽 로드됨, {len(split_docs)}개의 청크로 분할됨")

    print("******* 임베딩 및 벡터 DB 저장 중...")
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small",openai_api_key=openai_api_key)

    """
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=persist_path
    )
    """


    # 벡터스토어 빈 DB 먼저 생성
    vectordb = Chroma(
        embedding_function=embedding_model,
        persist_directory=persist_path
    )

    # 적당히 작은 단위로 나눠서 저장 (예: 100개씩)
    batch_size = 100
    for i in tqdm(range(0, len(split_docs), batch_size)):
        batch = split_docs[i:i+batch_size]
        vectordb.add_documents(batch)

    print("********** 벡터 DB 구축 완료!")


# 예시 실행
if __name__ == "__main__":
    build_vector_db(
        pdf_path="../생기부기재요령.pdf",
        persist_path="../vectordb",
    
    )
