from langchain_community.vectorstores import Chroma  
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def load_rag_chatbot(persist_path: str):
    embedding = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=openai_api_key,
    )
    vectordb = Chroma(persist_directory=persist_path, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1, openai_api_key=openai_api_key)

    prompt = ChatPromptTemplate.from_template("""
    당신은 교육부의 학교생활기록부 기재요령을 잘 아는 AI 비서입니다.
    아래 문서 내용(context)과 이전 대화(chat_history)를 바탕으로 사용자의 질문에 정중하고 정확하게 답하세요.

    - 먼저 사용자의 질문에 대해 **정확하고 간결한 답변**을 제공하세요.
    - 답변이 끝난 후, 반드시 context 중 참조한 문장을 아래 인용 형식으로 덧붙이세요.
    - 인용은 아래 형식을 따르세요:

    ---
    📘 **출처: 2025 생활기록부 기재요령**
    > 문장 1  
    > 문장 2  
    > 문장 3  
    ---

    [이전 대화]
    {chat_history}

    [문서 발췌]
    {context}

    [질문]
    {question}

    [답변]
    """)

    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])

    def qa_chain_with_memory(question):
        # 대화 불러오기
        chat_history = memory.load_memory_variables({}).get("chat_history", "")

        # 문서 검색 (한 번만 호출!)
        docs = retriever.get_relevant_documents(question)
        print("docs in module !!")
        print(docs)
        context = format_docs(docs)
        print("context in module!! ")
        print(context)

        # 체인 구성 후 실행
        result = prompt | llm
        response = result.invoke({
            "question": question,
            "context": context,
            "chat_history": chat_history
        })

        # 메모리 저장
        memory.save_context({"question": question}, {"answer": response.content})

        return {
            "answer": response.content,
            "source_documents": docs
        }

    return qa_chain_with_memory
