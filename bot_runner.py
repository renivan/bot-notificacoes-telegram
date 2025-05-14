import os
from telegram.ext import Application, CommandHandler
from supabase_client import log_admin_access, salvar_agendamento, cadastrar_usuario
from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv
# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
# Importar as funções necessárias do supabase_client
# e do dotenv
# Configuração do bot
# Certifique-se de que o arquivo .env contém TELEGRAM_TOKEN
# e que o token do bot do Telegram está correto

import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Comandos do bot
async def start(update, context):
    await update.message.reply_text("Olá! Eu sou seu bot de notificações.")

async def cadastrar(update, context):
    user = update.effective_user
    cadastrar_usuario(user.id, user.username)
    await update.message.reply_text("Cadastro realizado com sucesso!")

async def agendar(update, context):
    if len(context.args) < 2:
        await update.message.reply_text("Uso correto: /agendar <data> <mensagem>")
        return
    data = context.args[0]
    msg = " ".join(context.args[1:])
    salvar_agendamento(data, msg)
    await update.message.reply_text(f"Agendamento salvo para {data}.")

async def log(update, context):
    log_admin_access(update.effective_user.username)
    await update.message.reply_text("Log de acesso do admin salvo.")

def run_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cadastrar", cadastrar))
    application.add_handler(CommandHandler("agendar", agendar))
    application.add_handler(CommandHandler("log", log))
    asyncio.run(_run_bot(application))

async def _run_bot(application):
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.start_polling()
    await application.updater.idle()
    await application.updater.start_polling()
    await application.idle()
    await application.stop()
    await application.updater.stop()
    await application.shutdown()