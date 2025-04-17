import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import autenticar_usuario
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Login - LigaFut", layout="centered")

# 🔐 Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🎯 Layout centralizado com estilo
st.markdown("<div style='padding-top: 100px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>Bem-vindo à LigaFut</h2>", unsafe_allow_html=True)

# 🔐 Bloco do formulário
with st.container():
    st.markdown(
        """
        <div style='max-width: 400px; margin: 0 auto; background-color: rgba(0, 0, 0, 0.6); 
                    padding: 30px; border-radius: 15px; color: white;'>
        """,
        unsafe_allow_html=True
    )

    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        sucesso, user_data = autenticar_usuario(email, senha, db)
        if sucesso:
            st.session_state.usuario_id = user_data.get("id", "")
            st.session_state.usuario = user_data.get("usuario", "")  # necessário para tela Home
            st.session_state.nome_time = user_data.get("nome_time", "")
            st.session_state.id_time = user_data.get("id_time", "")
            st.success("Login realizado com sucesso!")
            switch_page("Elenco")
        else:
            st.error("E-mail ou senha incorretos.")

    st.markdown("</div>", unsafe_allow_html=True)
