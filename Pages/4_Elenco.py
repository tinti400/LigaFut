import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import registrar_movimentacao

st.set_page_config(page_title="Elenco - LigaFut", layout="wide")

# 🔐 Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🚧 Verifica se o usuário está logado
if "usuario_id" not in st.session_state or not st.session_state.usuario_id:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.stop()

usuario_id = st.session_state.usuario_id
id_time = st.session_state.id_time
nome_time = st.session_state.nome_time

st.title(f"📋 Elenco do {nome_time}")

# 🔄 Busca elenco do Firebase
elenco_ref = db.collection("times").document(id_time).collection("elenco").stream()
elenco = [doc.to_dict() | {"id": doc.id} for doc in elenco_ref]

if not elenco:
    st.info("Nenhum jogador cadastrado no elenco.")
    st.stop()

# 🟢 Exibição estilo planilha
st.markdown("---")
for jogador in elenco:
    col1, col2, col3, col4, col5 = st.columns([1.2, 3, 1.2, 2, 1.5])

    with col1:
        st.markdown(f"**{jogador.get('posição', '-')[:3]}**")
    with col2:
        st.markdown(f"**{jogador.get('nome', '-')}**")
    with col3:
        st.markdown(f"⭐ {jogador.get('overall', 0)}")
    with col4:
        st.markdown(f"💰 R$ {jogador.get('valor', 0):,.0f}".replace(",", "."))
    with col5:
        if st.button("Vender", key=f"vender_{jogador['id']}"):
            valor_total = jogador["valor"]
            valor_recebido = int(valor_total * 0.7)

            time_ref = db.collection("times").document(id_time)
            saldo_atual = time_ref.get().to_dict().get("saldo", 0)
            time_ref.update({"saldo": saldo_atual + valor_recebido})

            db.collection("mercado_transferencias").add(jogador)
            db.collection("times").document(id_time).collection("elenco").document(jogador["id"]).delete()

            registrar_movimentacao(db, id_time, "venda_mercado", jogador["nome"], valor_recebido)

            st.success(f"{jogador['nome']} vendido por R$ {valor_recebido:,.0f}".replace(",", "."))
            st.experimental_rerun()
