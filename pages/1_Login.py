import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.set_page_config(page_title="Login - LigaFut", page_icon="⚽")

st.markdown("<h2 style='text-align: center;'>🔐 Login - LigaFut</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

with st.form("login_form"):
    usuario = st.text_input("Usuário (e-mail)")
    senha = st.text_input("Senha", type="password")
    botao_login = st.form_submit_button("Entrar")

if botao_login:
    if usuario and senha:
        try:
            usuarios_ref = db.collection("usuarios").stream()
            usuario_encontrado = None
            for doc in usuarios_ref:
                dados = doc.to_dict()
                if dados.get("usuario") == usuario and dados.get("senha") == senha:
                    usuario_encontrado = doc
                    break

            if usuario_encontrado:
                st.success("✅ Login realizado com sucesso!")
                st.session_state["usuario"] = usuario
                st.session_state["id_usuario"] = usuario_encontrado.id
                st.switch_page("pages/4_Elenco.py")
            else:
                st.error("❌ Usuário ou senha incorretos. Verifique os dados.")
        except Exception as e:
            st.error(f"Erro ao acessar o banco de dados: {e}")
    else:
        st.warning("Preencha todos os campos.")
