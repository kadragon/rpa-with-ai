import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from io import BytesIO
import PyPDF2


def read_pdf(file):
    """PDF 파일의 텍스트를 추출하여 반환합니다."""
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:  # 페이지에서 텍스트를 성공적으로 추출했을 때만 추가
            text += page_text
    return text


def main():
    # Streamlit UI 구성
    with st.sidebar:
        openai_api_key = st.text_input(
            "OpenAI API Key", key="chatbot_api_key", type="password")
        st.markdown(
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

    st.title("💬 RPA with AI")
    st.caption("🚀 RPA with AI powered by kadragon")
    st.subheader('공문 분석기')

    uploaded_file = st.file_uploader("공문을 업로드하세요 (PDF 형식)", type=("pdf"))

    if uploaded_file and openai_api_key:
        try:
            # PDF 파일 읽기 및 텍스트 추출
            text = read_pdf(uploaded_file)

            # LangChain을 사용하여 텍스트를 처리
            llm = ChatOpenAI(model_name="gpt-4o-mini",
                             temperature=0, openai_api_key=openai_api_key)

            prompt = PromptTemplate.from_template(

                """ 
You are an AI assistant specialized in analyzing and summarizing official documents. Your task is to provide a concise and structured summary of the given document. Please follow these guidelines:

1. Provide a summary in the following format:

```markdown
# 공문 제목 (원문의 공문 제목을 정확히 기재)

## 🙋‍♂️ 관련
- 관련 문서가 있는 경우에만 작성하며, 없으면 "관련 문서 없음"으로 표기
- 발신처, 문서번호, 날짜 사이에 띄어쓰기를 하지 않음
- 형식: [[문서번호(YYYY.MM.DD)]] 공문제목 or 「규정명」 제조(항목)
- 예시: 
  - 1. [[XXXX-1234(2024.01.02)]] 공문제목
  - 2. [[XXXX-4567(2024.03.07)]] 공문제목
  - 3. 「한국교원대학교 교육정보원 규정」 제5조(직무)

## 공문번호
- 제공된 텍스트의 하단에 있음
- 형식: 발신처문서번호(YYYY.MM.DD)
- 발신처, 문서번호, 날짜 사이에 띄어쓰기를 하지 않음
- 예시: 교육정보원-955(2024.03.06)

## 📢 현황 및 문제점
- 핵심 내용을 3~5줄(- 으로 구분) 이내로 요약
- 주요 결정사항, 정책 변경, 또는 요구사항을 중심으로 작성

## 🛠 해결 방안
- 문서에서 명시적으로 언급된 후속 조치나 할일 사항을 나열
- 후속 조치 사항이 없는 경우 해결 방안 절을 생략
- 예시:
  - [ ] 할일 1 📅 YYYY-MM-DD
  - [ ] 할일 2 📅 YYYY-MM-DD
```

2. Carefully analyze the following text:
{texts}
"""
            )

            chain = prompt | llm

            # 결과 출력
            response = chain.invoke({"texts": text})
            st.markdown(response.content)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("PDF 파일과 OpenAI API Key를 모두 입력해야 합니다.")


if __name__ == "__main__":
    main()
