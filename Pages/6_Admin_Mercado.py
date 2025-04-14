import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login, verificar_leilao_ativo

st.set_page_config(page_title="Administração do Mercado", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

verificar_login()

st.title("🔧 Administração do Mercado de Transferências")

# Verifica se há leilão ativo
if verificar_leilao_ativo():
    st.warning("⚠️ Atenção: Leilão Ativo!")

# Buscar status do mercado
mercado_ref = db.collection("configuracoes").document("mercado")
mercado_doc = mercado_ref.get()

mercado_aberto = False
if mercado_doc.exists:
    dados = mercado_doc.to_dict()
    mercado_aberto = dados.get("aberto", False)

st.markdown(f"### Status do Mercado: {'Aberto' if mercado_aberto else 'Fechado'}")

# Botões para abrir ou fechar o mercado
col1, col2 = st.columns(2)

with col1:
    if st.button("Abrir Mercado"):
        mercado_ref.set({"aberto": True})
        st.success("Mercado aberto com sucesso!")
        st.experimental_rerun()

with col2:
    if st.button("Fechar Mercado"):
        mercado_ref.set({"aberto": False})
        st.success("Mercado fechado com sucesso!")
        st.experimental_rerun()

# Exibir jogadores disponíveis no mercado
st.subheader("Jogadores no Mercado")

mercado = db.collection("mercado_transferencias").stream()

for doc in mercado:
    jogador = doc.to_dict()
    st.write(f"Nome: {jogador['nome']} | Posição: {jogador['posicao']} | Overall: {jogador['overall']} | Valor: R$ {jogador['valor']:,}")
