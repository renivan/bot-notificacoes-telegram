import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega o .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set in the .env file")
# Verifica se as variáveis de ambiente foram carregadas corretamente
MESSAGE = "Seja bem-vindo ao meu grupo! Aqui você encontrará informações sobre ofertas, promoções e muito mais! \n\n Para mais promoções e ofertas entre no site."

url_get_updates = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
url_send_message = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": MESSAGE,
}

response = requests.get(url_get_updates, timeout=10)
print(response.json())

response = requests.post(url_send_message, data=payload, timeout=10)
print(response.json())
