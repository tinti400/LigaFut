import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login

st.set_page_config(page_title="Propostas Recebidas", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Verifica login
verificar_login()

id_time = st.session_state.id_time
nome_time = st.session_state.nome_time

st.title("📨 Propostas Recebidas")
st.markdown(f"### Time: {nome_time}")

propostas_ref = db.collection("propostas").where("id_time_destino", "==", id_time)
propostas = propostas_ref.stream()

tem_propostas = False

for proposta in propostas:
    tem_propostas = True
    dados = proposta.to_dict()
    jogador = dados['jogador']
    valor = dados['valor']
    id_time_origem = dados['id_time_origem']

    st.subheader(f"{jogador['nome']} - {jogador['posicao']} - Overall {jogador['overall']}")
    st.write(f"Proposta: R$ {valor:,.0f}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"Aceitar Proposta - {jogador['nome']}", key=f"aceitar_{proposta.id}"):
            # Atualizar caixas
            time_origem_ref = db.collection("times").document(id_time_origem)
            time_destino_ref = db.collection("times").document(id_time)

            saldo_origem = time_origem_ref.get().to_dict().get("saldo", 0)
            saldo_destino = time_destino_ref.get().to_dict().get("saldo", 0)

            time_origem_ref.update({"saldo": saldo_origem - valor})
            time_destino_ref.update({"saldo": saldo_destino + valor})

            # Remover jogador do time destino
            elenco_destino_ref = time_destino_ref.collection("elenco")
            elenco_jogador_query = elenco_destino_ref.where("nome", "==", jogador['nome']).get()

            for doc in elenco_jogador_query:
                doc.reference.delete()

            # Adicionar jogador no time origem
            time_origem_ref.collection("elenco").add(jogador)

            # Remover proposta
            proposta.reference.delete()

            st.success("Proposta aceita com sucesso!")
            st.experimental_rerun()

    with col2:
        if st.button(f"Recusar Proposta - {jogador['nome']}", key=f"recusar_{proposta.id}"):
            proposta.reference.delete()
            st.warning("Proposta recusada!")
            st.experimental_rerun()

if not tem_propostas:
    st.info("Nenhuma proposta recebida no momento.")

