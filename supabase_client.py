import os
from supabase import create_client
from datetime import datetime

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def cadastrar_usuario(user_id, username):
    supabase.table("usuarios").insert({
        "user_id": user_id,
        "username": username
    }).execute()

def salvar_agendamento(data, mensagem):
    supabase.table("agendamentos").insert({
        "data": data,
        "mensagem": mensagem
    }).execute()

def log_admin_access(username):
    supabase.table("logs_acesso").insert({
        "admin_username": username,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()
def get_agendamentos():
    response = supabase.table("agendamentos").select("*").execute()
    return response.data