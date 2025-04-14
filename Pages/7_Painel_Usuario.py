import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login, verificar_leilao_ativo

st.set_page_config(page_title="Painel do Usuário", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

verificar_login()

st.title("⚙️ Painel do Usuário")

# Verifica se há leilão ativo
if verificar_leilao_ativo():
    st.warning("⚠️ Atenção: Leilão Ativo!")

nome_usuario = st.session_state.usuario
nome_time = st.session_state.nome_time

st.markdown(f"### Bem-vindo, {nome_usuario}!")
st.markdown(f"### Time: {nome_time}")

st.markdown("---")

st.markdown("#### Selecione a página que deseja acessar:")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("Pages/4_Elenco.py", label="Meu Elenco", icon="🎽")

with col2:
    st.page_link("Pages/5_Mercado_Transferencias.py", label="Mercado de Transferências", icon="💰")

with col3:
    st.page_link("Pages/8_Financas.py", label="Finanças", icon="💵")
