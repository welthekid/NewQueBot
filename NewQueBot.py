import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8203881199:AAELC7oYRfiqm2hKs4dp7TDGtxU1TkPWTG4"
PEXELS_API_KEY = "sv4ZJjjJuVbE1ypSxFHDw9fqENKAouSyFd98StbuDBm3dYq2iFFlpSEe"

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /image termo_de_busca")
        return

    query = " ".join(context.args)

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 1
    }

    try:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params
        )

        data = response.json()

        if "photos" in data and data["photos"]:
            image_url = data["photos"][0]["src"]["large"]
            await update.message.reply_photo(photo=image_url)
        else:
            await update.message.reply_text("No image found.")

    except Exception as e:
        print(e)
        await update.message.reply_text("Error while searching image.")

app = ApplicationBuilder().token(TOKEN).build()

# 🔹 Aqui mudou para "image"
app.add_handler(CommandHandler("image", image))

print("Bot iniciado...")
app.run_polling()