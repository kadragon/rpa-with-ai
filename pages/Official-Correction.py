import streamlit as st
from langchain_core.prompts import PromptTemplate
from src.components.layout import header, get_openai_api_key
from src.utils.llm import create_llm


def initialize_session_state():
    if 'responses' not in st.session_state:
        st.session_state['responses'] = []


def create_translation_chain(llm):
    prompt = PromptTemplate.from_template(
        """
전문 공문 첨삭 전문가로서, 대한민국 행정안전부와 교육부 산하 국립대학의 고위 공무원이 부하 직원이 작성한 공문을 교정하고 교열하는 역할을 맡고 있습니다.

지침:
명확한 전달: 공문의 목적과 내용을 명확하게 전달할 수 있도록 문장을 다듬어 주세요.
어문규범 준수: 어문규범에 맞게 한글로 작성하되, 뜻을 정확하게 전달하기 위해 필요한 경우 괄호 안에 한자나 외국어를 함께 적어 주세요.
간결하고 명확한 표현: 문서의 내용은 간결하고 명확하게 표현하며, 일반화되지 않은 약어와 전문용어의 사용을 피하여 이해하기 쉽게 작성해야 합니다.
추가 정보 제공: 필요한 경우, 독자가 이해하기 쉽게 추가적인 정보나 설명을 덧붙여 주세요.
항목 구분: 문서 내용 구분 필요시 상위 항목부터 하위 항목까지 1., 가., 1), 가), (1), (가), ①, ㉮의 형태로 표시합니다. 필요 시 □, ○, -, ㆍ 등의 특수 기호로 표시할 수 있습니다.
금액 표기: 금액은 (예시: 금113,560원(금일십일만삼천오백육십원)) 형식으로 표기해 주세요.
날짜 및 시간 표기: 날짜는 YYYY. m. d. 형식으로, 시간은 HH24:MI 형식으로 표기해 주세요.
문서 종료 표시: 본문의 내용(본문에 붙임이 있는 경우에는 붙임을 말한다)의 마지막 글자에서 한 글자 띄우고 “끝” 표시를 합니다.
법률의 조항호 사이는 띄어쓰지 않음: 동법, 동조 => 같은 법, 같은 조로 순화합니다.
항목이 하나만 있는 경우 항목기호를 부여하지 않음: 항목이 하나일 경우 기호를 사용하지 않습니다.

이 지침을 바탕으로 공문을 전문적이고 효과적인 문서로 완성해 주세요. 첨삭 후, 수정된 내용을 간단히 요약하여 주시면 좋습니다.

기대 결과:
교정된 공문은 명확하고 간결하며, 독자가 쉽게 이해할 수 있도록 작성되어야 합니다.
수정된 내용의 요약은 간단하고 직관적으로 전달되어야 합니다.
이와 같은 형식으로 공문을 첨삭해 주시기 바랍니다.

공문제목: {title}

공문내용: {input}
"""
    )
    return prompt | llm


def main():
    header()
    st.subheader('공문 첨삭')
    st.info('작성한 공문을 교정, 교열, 맞춤법 검사 등을 해줍니다.')

    initialize_session_state()
    api_key = get_openai_api_key()

    with st.form('Question'):
        title = st.text_area('공문 제목', height=30)
        text = st.text_area('공문 내용', height=200)
        submitted = st.form_submit_button('보내기')

    if submitted and api_key:
        llm = create_llm(api_key)
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
