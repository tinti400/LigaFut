import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login

st.set_page_config(page_title="Meu Elenco", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Verificação de login
verificar_login()

# Buscar status do mercado
mercado_ref = db.collection("configuracoes").document("mercado")
mercado_doc = mercado_ref.get()
mercado_aberto = mercado_doc.to_dict().get("aberto", False) if mercado_doc.exists else False

# Dados do usuário logado
id_usuario = st.session_state.usuario_id
id_time = st.session_state.id_time
nome_time = st.session_state.nome_time

st.title("🎽 Meu Elenco")
st.markdown(f"### Time: {nome_time}")

elenco_ref = db.collection("times").document(id_time).collection("elenco")
elenco = [doc.to_dict() for doc in elenco_ref.stream()]

if not elenco:
    st.warning("Seu elenco está vazio.")
else:
    for jogador in elenco:
        posicao = jogador.get('posicao', 'Posição Desconhecida')
        with st.expander(f"{jogador['nome']} - {posicao} - Overall {jogador['overall']} - Valor R$ {jogador['valor']:,}"):
            if mercado_aberto:
                if st.button(f"Vender {jogador['nome']} para o Mercado", key=f"vender_{jogador['nome']}"):
                    valor_venda = int(jogador['valor'] * 0.7)
                    # Atualizar saldo do time
                    time_ref = db.collection("times").document(id_time)
                    time_doc = time_ref.get()
                    saldo_atual = time_doc.to_dict().get("saldo", 0)
                    novo_saldo = saldo_atual + valor_venda
                    time_ref.update({"saldo": novo_saldo})
                    # Remover jogador do elenco
                    jogador_ref = elenco_ref.document(jogador['nome'])
                    jogador_ref.delete()
                    # Inserir jogador no mercado
                    mercado_ref = db.collection("mercado_transferencias").document()
                    mercado_ref.set(jogador)
                    st.success(f"{jogador['nome']} vendido por R$ {valor_venda:,.2f}")
                    st.rerun()
            else:
                st.info("Mercado de Transferências está fechado. Não é possível vender jogadores.")

