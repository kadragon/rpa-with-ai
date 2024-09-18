import streamlit as st
from langchain_openai import ChatOpenAI
from typing import Optional

# 기본 설정 상수화
DEFAULT_MODEL_NAME = 'gpt-4o-mini'
DEFAULT_TEMPERATURE = 0.2
DEFAULT_STREAMING = False


def initialize_llm(api_key: str, model_name: str = DEFAULT_MODEL_NAME, temperature: float = DEFAULT_TEMPERATURE, streaming: bool = DEFAULT_STREAMING) -> Optional[ChatOpenAI]:
    """
    ChatOpenAI 인스턴스를 초기화합니다.

    Args:
        api_key (str): OpenAI API 키
        model_name (str): 사용할 모델 이름 (기본값: "gpt-4o-mini")
        temperature (float): 생성 텍스트의 무작위성 정도 (기본값: 0.2)
        streaming (bool): 스트리밍 모드 사용 여부 (기본값: False)

    Returns:
        ChatOpenAI or None: 성공 시 ChatOpenAI 인스턴스, 오류 발생 시 None
    """
    try:
        llm = ChatOpenAI(model_name=model_name, temperature=temperature,
                         openai_api_key=api_key, streaming=streaming)
        return llm
    except Exception as e:
        # 로그 파일에 오류 기록
        st.error(f"LLM 초기화 중 문제가 발생했습니다. {str(e)}")
        return None
