import os
import telebot
import requests
from dotenv import load_dotenv
from ModeloYOLO import ModeloYOLO
import json
from pymongo import MongoClient

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
FOTOS_DIR = "telegram_photos"
MONGO_URI = os.getenv("MONGO_URI")


if not os.path.exists(FOTOS_DIR):
    os.makedirs(FOTOS_DIR)

bot = telebot.TeleBot(TOKEN)

client = MongoClient(MONGO_URI)
db = client["chatbot"]
collection = db["datos"]


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, "¡Hola! Envíame una foto y la procesaré.")
    print(f"==============> Current user: {os.geteuid()}")


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

    data_to_insert = {
        "file_id": file_id,
        "photo_path": photo_path,
    }

    collection.insert_one(data_to_insert)

    ModeloYOLO(photo_path, file_id).predict()
    json_path = f"predictions/{file_id}/{file_id}.json"

    if not os.path.exists(json_path):
        bot.reply_to(
            message, "No se ha podido procesar la foto. Por favor, inténtalo de nuevo."
        )
    else:
        with open(json_path) as json_file:
            data = json.load(json_file)

        ingredientes = []
        for ingredient in data:
            ingredientes.append(ingredient["name"])
        bot.reply_to(
            message,
            f'Foto procesada! Nuestro modelo ha detectado que en la foto hay: {", ".join(ingredientes)}',
        )

        chat_id = message.chat.id
        img = open(f"predictions/{file_id}/image0.jpg", "rb")
        bot.send_photo(chat_id, img)


if __name__ == "__main__":
    print("Telegram bot is running...")
    bot.infinity_polling()
    print("Telegram bot is stopped.")
