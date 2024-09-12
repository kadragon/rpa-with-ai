import streamlit as st
from langchain_core.prompts import PromptTemplate
from src.components.layout import header, get_openai_api_key
from src.utils.llm import initialize_llm


def initialize_session_state():
    if 'responses' not in st.session_state:
        st.session_state['responses'] = []


def create_translation_chain(llm):
    prompt = PromptTemplate.from_template(
        """
아래 지침을 따라 영어 신문 기사를 한국어로 번역해주세요:

1. 형식:
   - 제목은 ### 로 표시
   - 소제목이 있을 경우 #### 로 표시
   - 본문은 단락별로 구분하여 번역
   - 불필요한 빈 줄이나 원문에 없는 내용 추가 금지

2. 번역 스타일:
   - 직역을 피하고 한국 독자들이 이해하기 쉽도록 자연스럽게 의역
   - 한국 언론사의 기사 스타일을 참고하여 번역
   - 공식적이고 객관적인 톤을 유지하되, 원문의 뉘앙스를 잘 전달할 것

3. 문화적 맥락:
   - 미국 특유의 표현이나 문화적 참조가 있을 경우, 한국 독자들이 이해할 수 있도록 간단히 설명 추가
   - 필요시 괄호 안에 부연 설명 제공

4. 전문 용어:
   - 경제, 정치, 과학 등 전문 분야의 용어는 한국에서 통용되는 번역어 사용
   - 적절한 한국어 용어가 없을 경우, 원어를 병기하고 설명 추가
   
5. 핵심 키워드:
   - 기사의 핵심 내용을 대표하는 3-5개의 키워드 추출
   - 각 키워드는 1단어로 구성하여 # 기호와 함께 나열

결과 예시:
```markdown
### [한국어 제목]

[번역된 본문 내용]

#### [소제목 (필요시)]

[소제목 관련 번역된 내용]

#### 핵심 키워드
#키워드1 #키워드2 #키워드3 #키워드4 #키워드5

```

원문:
{input}
"""
    )
    return prompt | llm


def main():
    header()
    st.subheader('News Translation')

    initialize_session_state()
    api_key = get_openai_api_key()

    with st.form('Question'):
        text = st.text_area('NYT News')
        submitted = st.form_submit_button('보내기')

    if submitted and api_key:
        llm = initialize_llm(api_key)
        if llm:
            chain = create_translation_chain(llm)
            with st.spinner('번역 중...'):
                try:
                    response = chain.invoke({"input": text})
                    st.session_state['responses'].append(response.content)
                except Exception as e:
                    st.error(f"번역 중 오류 발생: {str(e)}")

    st.markdown('\n'.join(st.session_state['responses']))


if __name__ == "__main__":
    main()
