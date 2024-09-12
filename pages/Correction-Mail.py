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
“전문적인 직장 커뮤니케이션 전문가로서, 직장 상사나 동료에게 보낼 이메일이나 메시지를 교정하고 수정해 주세요. 수정 이유와 함께 다음 번 작성 시 고려하면 좋을 팁도 제공해 주세요.”

지침:

맞춤법 및 문법 검사: 철저히 맞춤법, 오탈자, 문법 오류를 확인하고 수정합니다. 외래어는 가능한 한 사용을 자제해 주세요.
인사말 작성: 메시지는 반드시 인사말로 시작해야 합니다. 예: "안녕하세요. 인사팀 XXX입니다."와 같은 형식을 사용합니다.
명확성 및 핵심 전달: 두괄식으로 작성해 메일의 목적과 결론을 첫 문단에 명확하게 제시합니다. 요약을 추가해 수신자가 내용을 빠르게 파악할 수 있게 합니다.
간결성 유지: 메시지는 최대한 간결하게 작성합니다. 불필요한 단어나 문장을 제거하고, 초안을 작성한 후 다시 읽으며 필요 없는 부분을 삭제합니다.
구조화 및 가독성: 중요한 내용은 굵은 글씨나 밑줄 등을 사용해 강조합니다. 긴 문장은 뒷부분에 배치해 수신자가 선택적으로 읽을 수 있도록 합니다.
수신자 중심 작성: 수신자의 입장에서 메시지를 작성합니다. 그들이 알고 싶어 하는 정보에 집중하고, 발신자 중심의 내용이 아닌 수신자에게 가치를 제공하는 방향으로 작성합니다.

목표:
이 지침에 따라 직장에서 명확하고 효과적인 의사소통이 이루어지도록 이메일이나 메시지를 교정하고 수정해 주세요. 또한, 각 수정 사항에 대해 왜 그렇게 수정하였는지 설명하고, 다음 번에 글을 작성할 때 참고할 수 있는 팁도 함께 제공해 주세요.

메일제목: {title}

메일내용: {input}
"""
    )
    return prompt | llm


def main():
    header()
    st.subheader('메일/메시지 첨삭')
    st.info('작성한 메일/메시지를 교정, 교열, 맞춤법 검사 등을 해줍니다.')

    initialize_session_state()
    api_key = get_openai_api_key()

    with st.form('Question'):
        title = st.text_area('메일/메시지 제목', height=30)
        text = st.text_area('메일/메시지 내용', height=200)
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
