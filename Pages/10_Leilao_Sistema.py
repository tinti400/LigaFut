import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import time

st.set_page_config(page_title="Leilão do Sistema", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("⚽ Leilão do Sistema")

# Verificar se há leilão ativo
leilao_ref = db.collection("configuracoes").document("leilao_sistema")
leilao_doc = leilao_ref.get()

if leilao_doc.exists:
    leilao = leilao_doc.to_dict()
    if leilao.get("ativo", False):
        jogador = leilao.get("jogador")
        if jogador:
            st.subheader(f"Jogador: {jogador['nome']} - {jogador['posicao']} - Overall {jogador['overall']}")

            lance_atual = leilao.get("lance_atual", jogador["valor"])
            tempo_final = leilao.get("tempo_final")

            if tempo_final:
                segundos_restantes = int(tempo_final - time.time())
                if segundos_restantes < 0:
                    segundos_restantes = 0

                st.write(f"Valor Atual: R$ {lance_atual:,.0f}")
                st.write(f"Tempo restante: {segundos_restantes} segundos")

                ultimo_lance = leilao.get("ultimo_lance")
                if ultimo_lance:
                    st.write(f"Último Lance: {ultimo_lance}")

                if segundos_restantes > 0:
                    novo_lance = st.number_input("Digite o valor do lance", min_value=lance_atual + 100_000, step=100_000)

                    if st.button("Dar Lance"):
                        usuario = st.session_state.usuario
                        id_time = st.session_state.id_time
                        novo_tempo = tempo_final + 15 if segundos_restantes <= 15 else tempo_final

                        leilao_ref.update({
                            "lance_atual": novo_lance,
                            "ultimo_lance": usuario,
                            "id_time_vencedor": id_time,
                            "tempo_final": novo_tempo
                        })

                        st.success("Lance efetuado com sucesso!")
                        st.rerun()

                else:
                    if leilao.get("id_time_vencedor"):
                        vencedor = leilao["id_time_vencedor"]

                        # Atualizar valor do jogador com valor final do lance
                        jogador["valor"] = lance_atual

                        # Inserir jogador no elenco do time vencedor
                        db.collection("times").document(vencedor).collection("elenco").add(jogador)

                        # Atualizar saldo do time vencedor
                        time_ref = db.collection("times").document(vencedor)
                        time_doc = time_ref.get()
                        if time_doc.exists:
                            saldo_atual = time_doc.to_dict().get("saldo", 0)
                            time_ref.update({"saldo": saldo_atual - lance_atual})

                        # Finalizar leilão
                        leilao_ref.update({
                            "ativo": False,
                            "jogador": None,
                            "lance_atual": None,
                            "ultimo_lance": None,
                            "id_time_vencedor": None,
                            "tempo_final": None
                        })

                        st.success("Leilão finalizado! Jogador transferido.")
                        st.rerun()

            else:
                st.warning("Leilão configurado incorretamente.")
        else:
            st.warning("Leilão não configurado corretamente.")
    else:
        st.info("Nenhum leilão ativo no momento.")
else:
    st.warning("Leilão não configurado.")
