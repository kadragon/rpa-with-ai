import streamlit as st
from langchain_openai import ChatOpenAI


def create_llm(api_key, streaming=False):
    try:
        return ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2, openai_api_key=api_key, streaming=streaming)
    except Exception as e:
        st.error(f"Error creating LLM: {str(e)}")
        return None
