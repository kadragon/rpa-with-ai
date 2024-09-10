import streamlit as st


def header():
    st.title("💬 RPA with AI")
    st.caption("🚀 RPA with AI powered by kadragon")


def get_openai_api_key():
    with st.sidebar:
        openai_api_key = st.text_input(
            "OpenAI API Key", key="chatbot_api_key", type="password")
        st.markdown(
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
        if not openai_api_key:
            st.warning('OPEN API KEY를 입력해주시기 바랍니다.')
    return openai_api_key
