import os
import telebot
import requests
from dotenv import load_dotenv
from ImagePIL import bytes_2_image, string_to_bytes
from MongoDB import MongoDB

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
FOTOS_DIR = os.getenv("FOTOS_DIR")
API_YOLO = os.getenv("API_YOLO")


if not os.path.exists(FOTOS_DIR):
    os.makedirs(FOTOS_DIR)


bot = telebot.TeleBot(TOKEN)

mongodb = MongoDB()


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(
        message,
        "Hello! I'm a bot to detect ingredients in your photos. Please, send me a photo and I'll try to tell you what ingredients are in it.",
    )
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

    modeloYOLO = requests.post(
        API_YOLO, files={"file": open(photo_path, "rb")}, data={"file_id": file_id}
    )

    print("modeloYOLO =====>", modeloYOLO.status_code)

    data = modeloYOLO.json()

    if modeloYOLO.status_code != 200:
        bot.reply_to(
            message, "Sorry, I couldn't process your photo. Please, try again."
        )
    else:
        ingredient_list = []
        for ingredient in data:
            ingredient_list.append(ingredient["ingredient"])

        bot.reply_to(
            message,
            f'Proccessed photo! We have detected the following ingredients: {", ".join(ingredient_list)}',
        )

        chat_id = message.chat.id
        bytes_img = string_to_bytes(data[0]["image_bytes"])
        img = bytes_2_image(bytes_img)
        bot.send_photo(chat_id, img)

        ingredient_upper = [ingredient.capitalize() for ingredient in ingredient_list]

        recipes = list(mongodb.find_recipes_by_ingredients(ingredient_upper))

        for receta in recipes:
            title = receta["title"]
            ingredients_recipe = receta["ingredients"]
            directions_recipe = receta["directions"]

            # Formatear ingredientes en Markdown
            formatted_ingredients = "\n".join(
                [f"- {ingredient}" for ingredient in ingredients_recipe]
            )

            # Formatear instrucciones en Markdown
            formatted_directions = "\n".join(
                [f"{i+1}. {step}" for i, step in enumerate(directions_recipe)]
            )

            # Combinar título, ingredientes y direcciones en un solo mensaje
            formatted_message = f"*{title}*\n\n**Ingredients:**\n{formatted_ingredients}\n\n**Instructions:**\n{formatted_directions}"

            bot.reply_to(message, formatted_message, parse_mode="Markdown")


if __name__ == "__main__":
    print("Telegram bot is running...")
    bot.infinity_polling()
    print("Telegram bot is stopped.")
