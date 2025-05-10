import os
import time
import requests
from datetime import datetime, timedelta
from supabase import create_client
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === 1. CARREGAR CONFIGURAÇÕES ===
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === 2. FUNÇÕES DE BANCO DE DADOS ===

def cadastrar_usuario(nome, email):
    data = {"nome": nome, "email": email}
    return supabase.table("usuarios").insert(data).execute()

def criar_agendamento(usuario_id, descricao, dias_no_futuro=1):
    data_agendada = datetime.now() + timedelta(days=dias_no_futuro)
    agendamento = {
        "usuario_id": usuario_id,
        "descricao": descricao,
        "data_agendada": data_agendada.isoformat()
    }
    return supabase.table("agendamentos").insert(agendamento).execute()

def registrar_log_admin(acao, ip=None, user_agent=None):
    log = {"acao": acao, "ip": ip, "user_agent": user_agent}
    supabase.table("logs_admin").insert(log).execute()

def verificar_notificacoes():
    notificacoes = supabase.table("notificacoes").select("*").eq("status", False).execute()
    for n in notificacoes.data:
        enviar_mensagem(n["mensagem"])
        supabase.table("notificacoes").update({"status": True}).eq("id", n["id"]).execute()

# === 3. ENVIAR MENSAGEM DIRETA PELO BOT ===

def enviar_mensagem(mensagem, chat_id=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Erro ao enviar mensagem:", response.text)
    else:
        print("Mensagem enviada com sucesso!")

# === 4. COMANDOS DO BOT ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Olá! Sou seu bot de notificações.")
    registrar_log_admin("Bot iniciado por usuário", ip=str(chat_id))

async def enviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("Use: /enviar <mensagem>")
        return
    enviar_mensagem(msg, chat_id=update.effective_chat.id)
    await update.message.reply_text("Mensagem enviada.")
    registrar_log_admin("Mensagem manual enviada via comando", ip=str(update.effective_chat.id))

# === 5. EXECUÇÃO PRINCIPAL ===

def iniciar_bot():
    print("Iniciando o bot...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("enviar", enviar))

    # Processa notificações automaticamente em segundo plano
    async def notificacoes_job(app):
        while True:
            verificar_notificacoes()
            await asyncio.sleep(10)

    import asyncio
    asyncio.get_event_loop().create_task(notificacoes_job(app))
    app.run_polling()

if __name__ == "__main__":
    iniciar_bot()
