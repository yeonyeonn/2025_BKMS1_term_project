# lifeRecord/Generating.py
import openai
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent  # 이 파일(Generating.py)의 절대 경로
DATA_DIR = BASE_DIR / "data"                 # data 폴더도 이 파일 기준으로 잡음
API_KEY_FILE = DATA_DIR / "api_key.txt"

def load_api_key(api_key_path):
    with open(api_key_path, "r", encoding="utf-8") as f:
        return f.read().strip()

OPENAI_API_KEY = load_api_key(API_KEY_FILE)
openai.api_key = OPENAI_API_KEY

def generate_life_record(student_info: dict, query_context: str, user_query: str) -> str:
    system_prompt = (
        "너는 고등학교 교사야. 아래 학생 정보를 바탕으로 생활기록부 문장을 작성해줘. "
        "형식은 문단 형태로 자연스럽게 작성하고, 구체적인 활동 위주로 작성해."
        "내용은 4문장 이내로 간략하게 작성해줘."
        "말투는 ~함. ~하였음. ~ㅁ 이런식으로 작성해야한다."
    )

    full_prompt = f"학생 정보:\n{student_info}\n\n질의 관련 데이터:\n{query_context}\n\n사용자 질의:\n{user_query}"

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7
        )

    except Exception as e:
        raise RuntimeError(f"OpenAI API 호출 중 오류 발생: {e}")

    return response.choices[0].message.content.strip()


# 필요시 아래와 같은 테스트 코드 추가 가능
#if __name__ == "__main__":
#    sample_student = {
#        "이름": "홍길동",
#        "학년": 2,
#        "반": 3,
#        "번호": 15,
#        "동아리": ["피타고라스 수학 동아리"],
#        "활동내용": ["친구들에게 피타고라스의 법칙을 증명하는 발표를 수행"]
#    }
#    sample_context = "2024년 1학기 동안 수학 동아리 활동 내역과 수상 기록을 포함합니다."
#    user_query = "2024년 1학기 수학 동아리인 피타고라스에 활동한 이원정 학생의 활동을 바탕으로 생활기록부를 작성해줘"
#    print(generate_life_record(sample_student, sample_context, user_query))
