import os
import telebot
import requests
from dotenv import load_dotenv
from ModeloYOLO import ModeloYOLO
import json

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
FOTOS_DIR = "telegram_photos"

if not os.path.exists(FOTOS_DIR):
    os.makedirs(FOTOS_DIR)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, "¡Hola! Envíame una foto y la procesaré.")


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    print(f"Recibida foto con file_id: {file_id}")
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    print(photo_url)
    photo_path = os.path.join(FOTOS_DIR, f"{file_id}.jpg")
    print("photo_path =====>", photo_path)
    response = requests.get(photo_url)
    with open(photo_path, "wb") as f:
        f.write(response.content)

    ModeloYOLO(photo_path, file_id).predict()
    json_path = f"predictions/{file_id}/{file_id}.json"
    with open(json_path) as json_file:
        # Carga el contenido del archivo JSON en una variable como un diccionario
        data = json.load(json_file)
    bot.reply_to(
        message,
        f"Foto procesada! Nuestro modelo ha detectado que en la foto hay: {data['name']}",
    )


if __name__ == "__main__":
    print("Telegram bot is running...")
    bot.infinity_polling()
    print("Telegram bot is stopped.")
