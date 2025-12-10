import streamlit as st

def load_css(css_file_path):
    with open(css_file_path) as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)
