import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login

st.set_page_config(page_title="Login", layout="centered")

if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("🔐 Login")

usuario = st.text_input("Usuário").strip().lower()
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    if usuario == "" or senha == "":
        st.warning("Preencha todos os campos!")
    else:
        usuarios_ref = db.collection("usuarios")
        docs = usuarios_ref.where("usuario", "==", usuario).where("senha", "==", senha).stream()

        user_encontrado = None

        for doc in docs:
            user_encontrado = doc

        if user_encontrado:
            dados_usuario = user_encontrado.to_dict()
            st.session_state.usuario = usuario
            st.session_state.usuario_id = user_encontrado.id

            # Verifica se o usuário tem um time vinculado
            id_time = dados_usuario.get("id_time")

            if id_time:
                time_ref = db.collection("times").document(id_time)
                time_doc = time_ref.get()

                if time_doc.exists:
                    dados_time = time_doc.to_dict()
                    st.session_state.id_time = id_time
                    st.session_state.nome_time = dados_time.get("nome")

                    st.success("Login realizado com sucesso! ✅")

                    st.page_link("Pages/7_Painel_Usuario.py", label="Ir para o Painel do Usuário", icon="🏠")
                    st.page_link("Pages/5_Mercado_Transferencias.py", label="Ir para o Mercado", icon="💰")
                else:
                    st.error("Seu time não foi encontrado. Solicite ao administrador.")
            else:
                st.error("Seu time não foi encontrado. Solicite ao administrador.")
        else:
            st.error("Usuário ou senha incorretos.")


