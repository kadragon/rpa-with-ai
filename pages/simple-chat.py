from langchain_openai import ChatOpenAI
import streamlit as st


with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 KNUE RPA with AI")
st.caption("🚀 KNUE RPA with AI powered by OpenAI")

st.subheader('뭐든지 질문하세요!')


def generate_response(input_text):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0,
                     openai_api_key=openai_api_key)
    response = llm.invoke(input_text)
    st.info(response)


with st.form('Question'):
    text = st.text_area(
        'Your question', 'What types of text models does OpenAI provide?')
    submitted = st.form_submit_button('보내기')

    if submitted:
        generate_response(text)
