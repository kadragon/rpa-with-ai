import streamlit as st
from langchain_core.prompts import PromptTemplate
from src.components.layout import header, get_openai_api_key
import src.components.session as st_session
from src.utils.llm import initialize_llm


def create_translation_chain(llm):
    prompt = PromptTemplate.from_template(
        """
당신은 대한민국 행정안전부와 교육부 산하 국립대학의 공무원이 작성한 공문을 교정하고 교열하는 역할을 맡고 있습니다. 공문이 명확하고 효과적으로 작성될 수 있도록, 다음 지침을 따르십시오.

지침:
- 명확한 전달: 공문의 목적을 명확하게 전달할 수 있도록 문장을 다듬고, 불필요한 중복을 피하십시오.
- 어문 규범 준수: 한글 맞춤법과 띄어쓰기 등 어문 규범을 준수하고, 필요할 경우 괄호 안에 한자(漢字) 또는 외국어를 병기하여 뜻을 정확하게 전달하십시오.
- 간결하고 명확한 표현: 장황한 표현을 피하고 간결한 문장으로 정리하며, 구어체는 사용하지 말고, 공문에 적합한 문어체를 유지하십시오.
- 일관된 어휘 사용: 한 문서 내에서 동일한 의미의 용어는 일관되게 사용하고, 같은 개념에 대해 여러 단어를 혼용하지 않도록 하십시오.
- 전문 용어 및 외래어 사용 제한: 약어와 외래어는 필요한 경우에만 사용하고, 처음 등장할 때 약어를 괄호로 풀어써 설명하십시오. (예: 전사적 자원 관리 시스템(ERP))
- 수동형 표현 지양: 불필요한 수동형 문장을 능동형으로 바꾸어, 문장을 더 명확하게 작성하십시오.
- 추가 정보 제공: 필요 시 독자가 이해하기 쉽도록 추가적인 정보나 설명을 덧붙이고, 이해가 어려운 용어가 있을 경우 간단하게 설명하십시오. (덧붙일때에는 '*'(단어)나 '※'(문장)를 활용)
- 항목 구분 및 체계적 나열: 문서 내용 구분 필요시 상위 항목부터 하위 항목까지 1., 가., 1), 가), (1), (가), ①, ㉮의 형태로 표시합니다. 필요 시 □, ○, -, ㆍ 등의 특수 기호로 체계적 나열 방식으로 구분하십시오. 항목이 하나만 있을 경우 항목 기호는 부여하지 마십시오.
- 금액 표기: 금액은 숫자와 함께 한글 병기를 하여 표기하십시오. (예: 금113,560원(금일십일만삼천오백육십원))
- 날짜 및 시간 표기: 날짜는 YYYY. m. d. 형식으로, 시간은 HH:24 형식으로 표기하십시오.
- 법령 및 규정 인용: 법령이나 규정을 인용할 때 띄어쓰기 없이 표기하며, "동법" 대신 "같은 법", "동조" 대신 "같은 조"로 순화해서 사용하십시오. (예: "같은 법 제3조")
- 문서 종료 표시: 문서의 본문이 끝나면 마지막 글자에서 한 칸 띄우고 “끝.”으로 명확하게 문서가 종료되었음을 표시하십시오.
- 맞춤법 및 띄어쓰기: 맞춤법과 띄어쓰기를 철저히 검토하여 오류가 없도록 하십시오.

첨삭 후 요약:
- 첨삭 후, 문서의 명확성, 간결성, 일관성, 그리고 어문 규범 준수 측면에서 수정된 주요 사항을 간단하게 요약하여 설명하십시오.

첨삭 할 공문 정보: 
- 공문 제목: {title}

- 공문 내용: {input}
"""
    )
    return prompt | llm


def main():
    SUBHEADER = 'Correction Official'
    SESSION_KEY = 'responses'

    header()
    st.subheader(SUBHEADER)
    st.info('작성한 공문을 교정, 교열, 맞춤법 검사 등을 해줍니다.')

    st_session.initialize_session_state(SESSION_KEY, [])

    if st_session.check_page_change(SUBHEADER):
        st_session.reset_session_state(SESSION_KEY, [])

    api_key = get_openai_api_key()

    with st.form('Question'):
        title = st.text_area('공문 제목', height=30)
        text = st.text_area('공문 내용', height=200)
        submitted = st.form_submit_button('보내기')

    if submitted and api_key:
        llm = initialize_llm(api_key)
        if llm:
            chain = create_translation_chain(llm)
            with st.spinner('교정/교열 중...'):
                try:
                    response = chain.invoke({"input": text, "title": title})
                    st.session_state['responses'].append(response.content)
                except Exception as e:
                    st.error(f"교정/교열 중 오류 발생: {str(e)}")

    for response in st.session_state['responses']:
        st.info(response)


if __name__ == "__main__":
    main()
