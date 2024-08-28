import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


def initialize_session_state():
    if 'responses' not in st.session_state:
        st.session_state['responses'] = []


def get_openai_api_key():
    with st.sidebar:
        openai_api_key = st.text_input(
            "OpenAI API Key", key="chatbot_api_key", type="password")
        st.markdown(
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    return openai_api_key


def create_llm(api_key, temperature=0):
    try:
        return ChatOpenAI(model_name="gpt-4o-mini", temperature=temperature, openai_api_key=api_key)
    except Exception as e:
        st.error(f"Error creating LLM: {str(e)}")
        return None


def create_translation_chain(llm):
    prompt = PromptTemplate.from_template(
        """
전문 공문 첨삭 전문가로서, 대한민국의 고위 공무원이 부하 직원이 작성한 공문을 교정하고 교열하는 역할을 맡고 있습니다.

지침:
- 명확한 전달: 공문의 목적과 내용을 명확하게 전달할 수 있도록 문장을 다듬어 주세요.
- 어문규범 준수: 어문규범에 맞게 한글로 작성하되, 뜻을 정확하게 전달하기 위해 필요한 경우 괄호 안에 한자나 외국어를 함께 적어 주세요.
- 간결하고 명확한 표현: 문서의 내용은 간결하고 명확하게 표현하며, 일반화되지 않은 약어와 전문용어의 사용을 피하여 이해하기 쉽게 작성해야 합니다.
- 추가 정보 제공: 필요한 경우, 독자가 이해하기 쉽게 추가적인 정보나 설명을 덧붙여 주세요.
- 항목 구분: 문서 내용 구분 필요시 상위 항목부터 하위 항목까지 1., 가., 1), 가), (1), (가), ①, ㉮의 형태로 표시합니다. 필요 시 □, ○, -, ㆍ 등의 특수 기호로 표시할 수 있습니다.
- 금액 표기: 금액은 (예시: 금113,560원(금일십일만삼천오백육십원)) 형식으로 표기해 주세요.
- 날짜 및 시간 표기: 날짜는 YYYY. m. d. 형식으로, 시간은 HH24:MI 형식으로 표기해 주세요.
- 문서 종료 표시: 본문의 내용(본문에 붙임이 있는 경우에는 붙임을 말한다)의 마지막 글자에서 한 글자 띄우고 “끝” 표시를 합니다.

이 지침을 바탕으로 공문을 전문적이고 효과적인 문서로 완성해 주세요. 첨삭 후, 수정된 내용을 간단히 요약하여 주시면 좋습니다.

공문제목: {title}

공문내용: {input}
"""
    )
    return prompt | llm


def main():
    st.title("💬 RPA with AI")
    st.caption("🚀 RPA with AI powered by kadragon")
    st.subheader('Official Correction')

    initialize_session_state()
    api_key = get_openai_api_key()

    with st.form('Question'):
        title = st.text_area('공문 제목')
        text = st.text_area('공문 내용')
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
