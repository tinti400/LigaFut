import streamlit as st
from utils import verificar_leilao_ativo

st.set_page_config(page_title="Home - LigaFut", layout="wide")

verificar_leilao_ativo()

st.markdown(
    """
    <div style='text-align: center; margin-top: 100px;'>
        <h1 style='font-size: 60px; color: black;'>LF</h1>
        <h2 style='color: black;'>Simule qualquer campeonato de futebol com seus amigos</h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.page_link("Pages/1_Login.py", label="Login", icon="🔐")
st.page_link("Pages/2_Cadastro.py", label="Cadastro", icon="📝")
