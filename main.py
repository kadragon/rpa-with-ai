import streamlit as st
from src.components.layout import header


def main():
    header()

    st.subheader('News-Translation')
    st.info('영문 뉴스를 번역해줍니다.')

    st.subheader('Correction-Official')
    st.info('공문을 교정, 교열 해줍니다.')

    st.subheader('Correction-Mail')
    st.info('메일이나 메시지 내용을 교정, 교열 해줍니다.')

    st.subheader('Prompt-Maker')
    st.info('프롬프트를 개선해줍니다.')


if __name__ == "__main__":
    main()
