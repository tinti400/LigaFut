import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import time

st.set_page_config(page_title="Administração - Leilão", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("🎯 Administração - Leilão")

# Verificar status do mercado
status_ref = db.collection("configuracoes").document("mercado")
status_doc = status_ref.get()

# Verifica se existe o campo status, se não existir define 'fechado'
status_data = status_doc.to_dict() if status_doc.exists else {}
status_atual = status_data.get("status", "fechado")

st.subheader(f"Status do Leilão: {'🟢 Aberto' if status_atual == 'aberto' else '🔴 Fechado'}")

if status_atual == "fechado":
    if st.button("Abrir Mercado"):
        status_ref.set({"status": "aberto"})
        st.success("Mercado aberto com sucesso!")
        st.rerun()
else:
    if st.button("Fechar Mercado"):
        status_ref.set({"status": "fechado"})
        st.success("Mercado fechado com sucesso!")
        st.rerun()

st.divider()

# Verificar se já existe leilão ativo
leilao_ref = db.collection("configuracoes").document("leilao_sistema")
leilao_doc = leilao_ref.get()
dados_leilao = leilao_doc.to_dict() if leilao_doc.exists else {}

if dados_leilao.get("ativo", False):
    st.warning("Leilão já está ativo! Controle o andamento pela tela do sistema.")
else:
    st.subheader("Criar Novo Leilão")

    nome = st.text_input("Nome do Jogador")
    posicoes = [
        "GL", "LD", "ZAG", "LE", "VOL", "MC",
        "MD", "ME", "PD", "PE", "SA", "CA"
    ]
    posicao = st.selectbox("Posição", posicoes)
    overall = st.number_input("Overall", min_value=60, max_value=99, step=1)
    valor = st.number_input("Valor Inicial (R$)", min_value=100000, step=100000)

    if st.button("Criar Leilão"):
        tempo_final = time.time() + 120  # 2 minutos

        leilao_ref.set({
            "ativo": True,
            "jogador": {
                "nome": nome,
                "posicao": posicao,
                "overall": overall,
                "valor": valor
            },
            "lance_atual": valor,
            "time_vencedor": None,
            "tempo_final": tempo_final
        })
        st.success("Leilão criado com sucesso!")
        st.rerun()
