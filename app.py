import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_leilao_ativo

st.set_page_config(page_title="LigaFut", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.markdown("""
    <style>
        .titulo {
            text-align: center;
            font-size: 50px;
            color: white;
            margin-bottom: 20px;
        }
        .subtitulo {
            text-align: center;
            font-size: 20px;
            color: white;
        }
        .btn-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }
        .stButton>button {
            background-color: #00aaff;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="titulo">LF</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitulo">Simule qualquer campeonato de futebol com seus amigos</h2>', unsafe_allow_html=True)

# Aviso de Leilão Ativo
if verificar_leilao_ativo():
    st.warning("⚠️ Atenção: Leilão do Sistema Ativo!")

col1, col2 = st.columns(2)

with col1:
    if st.button("Login"):
        st.switch_page("Pages/1_Login.py")

with col2:
    if st.button("Cadastro"):
        st.switch_page("Pages/2_Cadastro.py")
