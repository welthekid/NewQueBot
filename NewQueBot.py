import os
import requests
from flask import Flask
from threading import Thread

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# ===== CONFIG =====
TOKEN = os.getenv("8203881199:AAH6WWj9vLGAUP0eEla244gQwSSL_mrVjmk")
SERPER_API_KEY = os.getenv("f087848a0e6e0eeee43b621feda3fb7b2c4a572c")

if not TOKEN:
    raise ValueError("TOKEN não encontrado nos Secrets.")

if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY não encontrado nos Secrets.")

# ===== KEEP ALIVE =====
web_app = Flask('')

@web_app.route('/')
def home():
    return "Bot rodando!"

def run_web():
    web_app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ===== BUSCA DE IMAGEM =====
def buscar_imagem(query):

    url = "https://google.serper.dev/images"

    payload = {
        "q": query
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=15
        )

        data = response.json()

        print("RESPOSTA SERPER:", data)

        if "images" in data and len(data["images"]) > 0:
            return data["images"][0]["imageUrl"]

    except Exception as e:
        print("ERRO SERPER:", e)

    return None

# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Olá!\n\n"
        "Use:\n"
        "/image termo\n\n"
        "Exemplo:\n"
        "/image carro voador"
    )

# ===== /image =====
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Use: /image termo"
        )
        return

    query = " ".join(context.args)

    img = buscar_imagem(query)

    if img:
        try:
            await update.message.reply_photo(photo=img)

        except Exception as e:
            print("ERRO TELEGRAM:", e)

            await update.message.reply_text(
                f"Não consegui enviar a imagem diretamente.\n\n{img}"
            )
    else:
        await update.message.reply_text(
            "Nenhuma imagem encontrada."
        )

# ===== BOT =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("image", image)
)

# ===== INICIA =====
keep_alive()

print("Bot iniciado...")

app.run_polling()
