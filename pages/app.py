import streamlit as st
import os

# Deixe o título e fundo como quiser
st.set_page_config(
    page_title="LigaFut",
    page_icon="⚽",
    layout="wide"
)

# Conteúdo da Home
st.markdown("<h1 style='text-align: center;'>⚽ LigaFut</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Gerencie sua liga como um verdadeiro técnico!</h4>", unsafe_allow_html=True)

# Força exibição do menu lateral com as páginas
st.sidebar.success("Selecione uma opção acima ☝️")
