import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login

st.set_page_config(page_title="Negociações entre Clubes", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Verificar login
verificar_login()

st.title("🤝 Negociações entre Clubes")

# ID do time logado
id_time = st.session_state.id_time
nome_time = st.session_state.nome_time

st.markdown(f"### Seu Time: {nome_time}")

# Buscar todos os times
times_ref = db.collection("times").stream()
times = {doc.id: doc.to_dict().get("nome", "Sem Nome") for doc in times_ref}

# Exibir lista de times
for time_id, time_nome in times.items():
    if time_id == id_time:
        continue  # Não mostrar o próprio time

    with st.expander(f"Time: {time_nome}"):
        elenco_ref = db.collection("times").document(time_id).collection("elenco").stream()
        elenco = [jogador.to_dict() | {"id_doc": jogador.id} for jogador in elenco_ref]

        if not elenco:
            st.write("Nenhum jogador disponível neste time.")
        else:
            for jogador in elenco:
                nome = jogador.get("nome", "Sem nome")
                posicao = jogador.get("posicao", "Desconhecida")
                overall = jogador.get("overall", "N/A")
                valor = jogador.get("valor", 0)
                id_jogador = jogador.get("id_doc")

                st.markdown(f"**{nome}** | Posição: {posicao} | Overall: {overall} | Valor: R$ {valor:,.0f}")

                proposta = st.number_input(
                    f"💰 Valor da Proposta para {nome}",
                    min_value=1_000_000,
                    value=valor,
                    step=500_000,
                    key=f"proposta_valor_{id_jogador}"
                )

                if st.button(f"📨 Enviar Proposta por {nome}", key=f"confirmar_proposta_{id_jogador}"):
                    proposta_data = {
                        "id_time_origem": id_time,
                        "id_time_destino": time_id,
                        "id_jogador": id_jogador,
                        "valor_proposta": proposta,
                        "nome_jogador": nome,
                        "status": "pendente",
                        "timestamp": firestore.SERVER_TIMESTAMP,
                    }
                    db.collection("negociacoes").add(proposta_data)
                    st.success("Proposta enviada com sucesso!")


