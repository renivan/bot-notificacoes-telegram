from flask import Flask
from threading import Thread
from bot_runner import run_bot
from dotenv import load_dotenv
import os
import requests

load_dotenv('.env')
# from bot_runner import run_bot

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot Telegram está rodando com sucesso!'

if __name__ == '__main__':
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=8000)
# Inicia o bot em uma thread separada
# para não bloquear o servidor Flask

# Inicia o servidor Flask
port = int(os.environ.get("PORT", 8000))
app.run(host='0.0.0.0', port=port)