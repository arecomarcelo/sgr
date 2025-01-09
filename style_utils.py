import streamlit as st
from style_config import StyleConfig

def apply_default_style():
    """
    Aplica o estilo padrão em todas as páginas
    """
    st.markdown(StyleConfig.get_hide_streamlit_elements(), unsafe_allow_html=True)
