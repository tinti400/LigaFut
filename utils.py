import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Função para verificar se o usuário está logado
def verificar_login():
    if "usuario_id" not in st.session_state:
        st.error("Você precisa estar logado para acessar essa página.")
        st.stop()

# Função para verificar se o mercado está aberto
def verificar_mercado_aberto():
    config_ref = db.collection("configuracoes").document("mercado")
    config_doc = config_ref.get()
    if config_doc.exists:
        dados = config_doc.to_dict()
        return dados.get("status", "fechado") == "aberto"
    return False

# Função para verificar se existe um leilão ativo
def verificar_leilao_ativo():
    leilao_ref = db.collection("configuracoes").document("leilao")
    leilao_doc = leilao_ref.get()
    if leilao_doc.exists:
        dados = leilao_doc.to_dict()
        return dados.get("ativo", False)
    return False

# Função para buscar nome do time pelo id
def buscar_nome_time(id_time):
    time_ref = db.collection("times").document(id_time)
    time_doc = time_ref.get()
    if time_doc.exists:
        return time_doc.to_dict().get("nome", "Desconhecido")
    return "Desconhecido"
