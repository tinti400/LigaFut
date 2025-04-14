import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login, verificar_leilao_ativo

st.set_page_config(page_title="Finanças do Clube", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

verificar_login()

st.title("💰 Finanças do Clube")

# Verifica se há leilão ativo
if verificar_leilao_ativo():
    st.warning("⚠️ Atenção: Leilão Ativo!")

# Recupera informações do usuário logado
id_usuario = st.session_state.usuario_id
id_time = st.session_state.id_time
nome_time = st.session_state.nome_time

st.markdown(f"### Time: {nome_time}")

time_ref = db.collection("times").document(id_time)
time_doc = time_ref.get()

if time_doc.exists:
    dados_time = time_doc.to_dict()
    saldo = dados_time.get("saldo", 0)

    st.metric("Saldo Disponível", f"R$ {saldo:,.2f}")
else:
    st.error("Informações do time não encontradas.")

