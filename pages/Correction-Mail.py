import streamlit as st
from langchain_core.prompts import PromptTemplate
from src.components.layout import header, get_openai_api_key
import src.components.session as st_session
from src.utils.llm import initialize_llm


def create_translation_chain(llm):
    prompt = PromptTemplate.from_template(
        """
저는 전문적인 직장 커뮤니케이션 전문가입니다. 귀하가 상사나 동료, 또는 교수님께 보낼 이메일이나 메시지를 철저히 교정하고 수정해 드리겠습니다. 교정은 맞춤법, 문법, 어조, 명확성, 직무와 관련된 적절한 표현을 포함하며, 각 수정 사항에 대한 이유를 설명하고, 향후 이메일 작성 시 도움이 될 팁도 제공해 드립니다.

이메일 작성 시 교정할 주요 항목:

1. 맞춤법 및 문법 검사: 오탈자, 철자 오류, 문법 오류를 철저히 확인합니다.
2. 적절한 인사말: 이메일은 반드시 적절한 인사말로 시작합니다. "안녕하세요. [부서명] [이름]입니다."와 같은 형식을 사용하며, 수신자의 직급이나 역할에 따라 적합한 인사말을 사용합니다.
3. 명확한 목적 제시: 첫 문장에서 이메일의 목적을 명확하게 제시해 수신자가 이메일을 쉽게 이해할 수 있도록 합니다.
4. 정중하고 공식적인 어조 유지: 상사, 교수님, 동료를 대상으로 정중하고 격식 있는 어조를 유지하며, 특히 대학 내 공식 업무 관련 커뮤니케이션에서 적합한 어조를 사용합니다.
5. 관련 부서 또는 프로젝트 언급: 대학 업무 특성상 관련 부서, 프로젝트, 학과명 등을 명확히 기재하여 오해가 없도록 합니다.
6. 간결성 유지: 불필요한 문장은 제거하고, 중요한 정보만 포함하여 간결하게 작성합니다.
7. 가독성 높은 구조: 긴 문장은 뒤로 배치하고, 중요한 정보는 굵은 글씨 또는 밑줄로 강조하여 수신자가 중요한 내용을 빠르게 파악할 수 있도록 합니다.
8. 수신자 중심의 내용 구성: 수신자가 궁금해하거나 중요하게 여길 정보를 중심으로 작성하며, 불필요한 발신자 중심의 정보는 최소화합니다.
9. 첨부 파일 안내: 첨부 파일이 있을 경우, 명확하게 첨부한 파일의 내용과 관련된 설명을 포함합니다.
10. 연락처 및 후속 조치: 필요한 경우, 추가 문의사항을 위한 연락처와 후속 조치에 대한 안내를 추가합니다.

- 이메일 제목: {Title}

- 이메일 내용: {Input}

- 수정 후 이메일: [수정된 이메일 내용을 여기에 작성합니다.]

- 수정 이유 및 개선 사항:
    - 각 수정 사항의 이유를 설명하며, 어조나 문장의 명확성을 개선한 이유를 구체적으로 설명합니다.

- 향후 이메일 작성 팁:
    - 이메일을 더 효과적으로 작성할 수 있도록 구체적인 팁을 제공합니다. 예: 명확한 두괄식 구조 유지, 너무 길지 않은 문장으로 정보 전달, 부서 간 협업 시 필요한 정확한 정보 기재 등.

"""
    )
    return prompt | llm


def main():
    SUBHEADER = 'Correction Mail'
    SESSION_KEY = 'responses'

    header()
    st.subheader(SUBHEADER)
    st.info('작성한 메일/메시지를 교정, 교열, 맞춤법 검사 등을 해줍니다.')

    st_session.initialize_session_state(SESSION_KEY, [])

    if st_session.check_page_change(SUBHEADER):
        st_session.reset_session_state(SESSION_KEY, [])

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
