import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login, verificar_leilao_ativo

st.set_page_config(page_title="Mercado de Transferências", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

verificar_login()

st.title("💰 Mercado de Transferências")

# Verifica se há leilão ativo
if verificar_leilao_ativo():
    st.warning("⚠️ Atenção: Leilão Ativo!")

id_time = st.session_state.id_time
nome_time = st.session_state.nome_time

st.markdown(f"### Time: {nome_time}")

# Verificar se o mercado está aberto
mercado_ref = db.collection("configuracoes").document("mercado")
mercado_doc = mercado_ref.get()
mercado_aberto = False
if mercado_doc.exists:
    dados = mercado_doc.to_dict()
    mercado_aberto = dados.get("aberto", False)

if not mercado_aberto:
    st.warning("O Mercado de Transferências está fechado no momento.")
    st.stop()

# Filtros
filtro_nome = st.text_input("Buscar por Nome")
filtro_posicao = st.text_input("Buscar por Posição")
filtro_overall = st.slider("Filtrar Overall", 65, 99, (65, 99))

# Buscar jogadores do mercado
mercado = db.collection("mercado_transferencias").stream()

jogadores = []
for doc in mercado:
    jogador = doc.to_dict()
    jogador["id"] = doc.id
    jogadores.append(jogador)

# Aplicar Filtros
if filtro_nome:
    jogadores = [j for j in jogadores if filtro_nome.lower() in j["nome"].lower()]
if filtro_posicao:
    jogadores = [j for j in jogadores if filtro_posicao.lower() in j["posicao"].lower()]
jogadores = [j for j in jogadores if filtro_overall[0] <= j["overall"] <= filtro_overall[1]]

for jogador in jogadores:
    with st.expander(f"{jogador['nome']} - {jogador['posicao']} - Overall {jogador['overall']} - Valor R$ {jogador['valor']:,}"):
        if st.button(f"Comprar {jogador['nome']}", key=jogador['id']):
            # Buscar saldo do time
            time_ref = db.collection("times").document(id_time)
            time_doc = time_ref.get()
            if time_doc.exists:
                dados_time = time_doc.to_dict()
                saldo_atual = dados_time.get("saldo", 0)
                if saldo_atual >= jogador["valor"]:
                    novo_saldo = saldo_atual - jogador["valor"]
                    time_ref.update({"saldo": novo_saldo})

                    # Adiciona jogador ao elenco
                    elenco_ref = time_ref.collection("elenco")
                    elenco_ref.add(jogador)

                    # Remove jogador do mercado
                    db.collection("mercado_transferencias").document(jogador["id"]).delete()

                    st.success(f"{jogador['nome']} comprado com sucesso!")
                    st.experimental_rerun()
                else:
                    st.error("Saldo insuficiente para realizar a compra.")

        if st.button(f"Excluir {jogador['nome']} do Mercado", key=f"excluir_{jogador['id']}"):
            db.collection("mercado_transferencias").document(jogador["id"]).delete()
            st.success(f"{jogador['nome']} removido do mercado!")
            st.experimental_rerun()

