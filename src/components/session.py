import streamlit as st


# 세션 상태 관리 함수들을 리팩토링
def check_page_change(page_name):
    # 세션 상태 초기화
    initialize_session_state('current_page', '')

    # 이전 페이지 저장 및 현재 페이지 업데이트
    prev_page = st.session_state['current_page']
    st.session_state['current_page'] = page_name

    # 페이지 변경 여부 반환
    return prev_page != page_name


def initialize_session_state(key, value):
    # 세션 상태 초기화
    if key not in st.session_state:
        st.session_state[key] = value


def reset_session_state(key, value):
    # 세션 상태 리셋
    st.session_state[key] = value
