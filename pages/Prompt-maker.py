import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate


def create_llm(api_key):
    try:
        return ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=api_key)
    except Exception as e:
        st.error(f"Error creating LLM: {str(e)}")
        return None


def make_prompt():
    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system",
             "You are an expert Prompt Writer for Large Language Models."),
            ("human", """
        Your goal is to improve the prompt given below for {task} :
    --------------------

    Prompt: {lazy_prompt}

    --------------------

    Here are several tips on writing great prompts:

    -------

    Start the prompt by stating that it is an expert in the subject.

    Put instructions at the beginning of the prompt and use ### or to separate the instruction and context 

    Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style, etc 

    ---------

    Here's an example of a great prompt:

    As a master YouTube content creator, develop an engaging script that revolves around the theme of "Exploring Ancient Ruins."

    Your script should encompass exciting discoveries, historical insights, and a sense of adventure.

    Include a mix of on-screen narration, engaging visuals, and possibly interactions with co-hosts or experts.

    The script should ideally result in a video of around 10-15 minutes, providing viewers with a captivating journey through the secrets of the past.

    Example:

    "Welcome back, fellow history enthusiasts, to our channel! Today, we embark on a thrilling expedition..."

    -----

    Now, improve the prompt.
    
    반드시 한글로 대답해줘.

    IMPROVED PROMPT:
        """),
        ]
    )

    return chat_template


def main():
    # Streamlit UI 구성
    with st.sidebar:
        openai_api_key = st.text_input(
            "OpenAI API Key", key="chatbot_api_key", type="password")
        st.markdown(
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

    st.title("💬 RPA with AI")
    st.caption("🚀 RPA with AI powered by kadragon")
    st.subheader('프롬프트 생성기')

    with st.form('Question'):
        task = st.text_area('목표')
        lazy_prompt = st.text_area('프롬프트')
        submitted = st.form_submit_button('보내기')

    if openai_api_key == '':
        st.warning('API Key를 입력해 주세요!')

    if submitted and openai_api_key:
        llm = create_llm(openai_api_key)
        prompt = make_prompt()

        chain = prompt | llm

        with st.spinner('작업 중...'):
            try:
                response = chain.invoke(
                    {"task": task, "lazy_prompt": lazy_prompt})
                st.info(response.content)
            except Exception as e:
                st.error(f"작업 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
