import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 RPA with AI")
st.caption("🚀 RPA with AI powered by kadragon")
