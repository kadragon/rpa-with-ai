import streamlit as st
from langchain_core.prompts import PromptTemplate
from src.components.layout import header, get_openai_api_key
import src.components.session as st_session
from src.utils.llm import initialize_llm
from typing import Tuple

# ================================
# Constants
# ================================
SUBHEADER = 'Correction Mail'
SESSION_KEY = 'responses'
INFO_MESSAGE = '작성한 메일/메시지를 교정, 교열, 맞춤법 검사 등을 해줍니다.'

FORM_LABELS = {
    'title': '메일/메시지 제목',
    'text': '메일/메시지 내용',
    'submit': '보내기'
}

PROMPT_TEMPLATE = """
저는 전문적인 커뮤니케이션 전문가로서, 상사, 동료, 교수님께 보내는 이메일이나 메시지를 철저하게 교정하고 수정해 드립니다. 문법, 어조, 명확성, 직무 관련 적절한 표현을 중심으로 교정하며, 수정된 사항에 대한 설명과 더불어 향후 이메일 작성에 도움이 되는 팁도 제공해 드립니다.

이메일 교정 주요 항목:
1. 맞춤법 및 문법 검사: 철저한 오탈자, 맞춤법, 문법 오류 확인.
2. 적절한 인사말: 수신자의 직급이나 역할에 맞는 정중하고 적절한 인사말 작성.
3. 명확한 목적 제시: 이메일의 목적을 첫 문장에서 명확히 전달하여 수신자가 쉽게 이해할 수 있도록 함.
4. 정중하고 공식적인 어조 유지: 상사, 교수님, 동료에게 적합한 격식 있는 어조 유지.
5. 관련 부서/프로젝트 언급: 부서명, 프로젝트명 등 필요한 정보를 명확히 기재하여 오해 방지.
6. 간결성 유지: 불필요한 내용을 제거하고, 핵심 정보만 간결하게 전달.
7. 가독성 높은 구조: 중요 내용을 빠르게 파악할 수 있도록 문장을 적절히 나누고, 필요 시 굵은 글씨나 밑줄 사용.
8. 수신자 중심의 내용 구성: 수신자가 중요하게 여길 정보를 중심으로 작성, 불필요한 발신자 중심의 정보 최소화.
9. 첨부 파일 안내: 첨부 파일이 있을 경우, 파일의 내용과 목적을 명확하게 설명.
10. 연락처 및 후속 조치: 추가 문의나 후속 조치에 대한 연락처 안내.

수정 이유 및 향후 이메일 작성 팁:
- 수정 사항 설명: 각 수정 사항에 대해 명확한 이유를 제공하여 문장 명료성 및 어조를 개선한 이유 설명.
- 향후 이메일 작성 팁: 두괄식 구조, 짧고 명료한 문장 사용, 협업 시 필요한 정확한 정보 기재 등 구체적인 이메일 작성 팁 제공.

- 이메일 제목: {title}

- 이메일 내용: {input}
"""

# ================================
# Functions
# ================================


def create_prompt_template(template_str: str) -> PromptTemplate:
    """
    Creates a PromptTemplate object from a template string.

    Args:
        template_str (str): The prompt template string.

    Returns:
        PromptTemplate: The instantiated prompt template.
    """
    return PromptTemplate.from_template(template_str)


def create_correction_chain(llm) -> PromptTemplate:
    """
    Creates the correction chain by combining the prompt template with the LLM.

    Args:
        llm: The initialized language model.

    Returns:
        PromptTemplate: The combined prompt and LLM chain.
    """
    prompt = create_prompt_template(PROMPT_TEMPLATE)
    return prompt | llm


def render_form() -> Tuple[str, str, bool]:
    """
    Renders the input form for the user to enter email/message title and content.

    Returns:
        Tuple[str, str, bool]: The title, text, and submission status.
    """
    with st.form('correction_form'):
        title = st.text_area(
            FORM_LABELS['title'], height=50, help="이메일이나 메시지의 제목을 입력하세요.")
        text = st.text_area(
            FORM_LABELS['text'], height=200, help="교정이 필요한 이메일이나 메시지 내용을 입력하세요.")
        submitted = st.form_submit_button(FORM_LABELS['submit'])
    return title.strip(), text.strip(), submitted


def process_submission(title: str, text: str, api_key: str) -> None:
    """
    Processes the form submission by invoking the LLM to correct the text.

    Args:
        title (str): The title of the email/message.
        text (str): The content of the email/message.
        api_key (str): The OpenAI API key.
    """
    if not api_key:
        st.error("API 키가 제공되지 않았습니다.")
        return

    llm = initialize_llm(api_key)
    if not llm:
        st.error("LLM을 초기화하는 데 실패했습니다.")
        return

    chain = create_correction_chain(llm)
    with st.spinner('교정/교열 중...'):
        try:
            response = chain.invoke({"input": text, "title": title})
            if SESSION_KEY not in st.session_state:
                st.session_state[SESSION_KEY] = []
            st.session_state[SESSION_KEY].append(response.content)
        except Exception as e:
            st.error(f"교정/교열 중 오류 발생: {str(e)}")


def display_responses() -> None:
    """
    Displays all corrected responses stored in the session state.
    """
    responses = st.session_state.get(SESSION_KEY, [])
    for idx, response in enumerate(responses, 1):
        st.markdown(f"### 교정 {idx}")
        st.info(response)


def initialize_session() -> None:
    """
    Initializes the session state for storing responses.
    """
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = []


def reset_session_if_needed(current_page: str) -> None:
    """
    Resets the session state if the user navigates to a different page.

    Args:
        current_page (str): The identifier of the current page.
    """
    if st_session.check_page_change(current_page):
        st_session.reset_session_state(SESSION_KEY, [])


def main() -> None:
    """
    The main function that orchestrates the Streamlit app.
    """
    header()
    st.subheader(SUBHEADER)
    st.info(INFO_MESSAGE)

    initialize_session()
    reset_session_if_needed(SUBHEADER)

    api_key = get_openai_api_key()
    title, text, submitted = render_form()

    if submitted:
        if title and text:
            process_submission(title, text, api_key)
        else:
            st.warning("제목과 내용을 모두 입력해주세요.")

    display_responses()


if __name__ == "__main__":
    main()
