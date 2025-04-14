import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
cred = credentials.Certificate("credenciais.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Dados dos usuários com seus respectivos times
usuarios_times = {
    "atletico-mg@ligafut.com": {"id_time": "0fgitv421Pe4OWu6OYnm", "nome_time": "Atlético-MG"},
    "fortaleza@ligafut.com": {"id_time": "648H5LX98Rkd0DemlWEX", "nome_time": "Fortaleza"},
    "cruzeiro@ligafut.com": {"id_time": "6ScPtoiLBn27re1nLaOZ", "nome_time": "Cruzeiro"},
    "flamengo@ligafut.com": {"id_time": "6lLrThoafAocWJosvLh0", "nome_time": "Flamengo"},
    "bahia@ligafut.com": {"id_time": "7DzNqRL8bDu4bSMLpufj", "nome_time": "Bahia"},
    "gremio@ligafut.com": {"id_time": "91zvcBPDxfbWUuoZdYqd", "nome_time": "Grêmio"},
    "botafogo@ligafut.com": {"id_time": "9GP2DYELgPYVtonYZpKW", "nome_time": "Botafogo"},
    "saopaulo@ligafut.com": {"id_time": "BVwhAm54WYzY095vOUyT", "nome_time": "São Paulo"},
    "internacional@ligafut.com": {"id_time": "ENxH4QPxPvpyTFqMP4w8", "nome_time": "Internacional"},
    "palmeiras@ligafut.com": {"id_time": "Lqw71T9zWpqm8Iub2cLq", "nome_time": "Palmeiras"}
}

print("⏳ Atualizando usuários...")

for email, dados_time in usuarios_times.items():
    usuarios_ref = db.collection("usuarios")
    docs = usuarios_ref.where("usuario", "==", email).stream()
    
    encontrado = False
    for doc in docs:
        doc_ref = usuarios_ref.document(doc.id)
        doc_ref.update({
            "id_time": dados_time["id_time"],
            "nome_time": dados_time["nome_time"]
        })
        print(f"✅ Usuário {email} atualizado com sucesso!")
        encontrado = True

    if not encontrado:
        print(f"❌ Usuário {email} não encontrado.")

print("🏁 Processo finalizado!")

