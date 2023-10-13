import os
from dotenv import load_dotenv
from pymongo import MongoClient
import json
from random import sample

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["recipes"]
collection = db["recipes"]

with open("recipes.json") as json_file:
    data = json.load(json_file)


class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client["recipes"]
        self.collection = self.db["recipes"]
        self.collection.insert_many(data)

    def find_recipes_by_ingredients(self, ingredient_list):
        """
        Busca 5 recetas aleatorias bajas en grasa por ingredientes en la base de datos MongoDB.

        Args:
            ingredient_list (list): Lista de ingredientes a buscar.

        Returns:
            list: Una lista con 5 recetas aleatorias bajas en grasa.
        """
        # Agrega la etapa $match para encontrar recetas bajas en grasa
        pipeline = [
            {
                "$match": {"categories": {"$in": ingredient_list}, "fat": {"$lt": 5}}
            },  # Ajusta el valor 5 según tus criterios de "bajas en grasa"
            {
                "$sample": {"size": 5}
            },  # Obtiene 5 recetas aleatorias de las que coinciden con el filtro
        ]

        # Ejecuta la agregación
        cursor = self.collection.aggregate(pipeline)

        # Convierte el cursor a una lista de recetas
        random_low_fat_recipes = list(cursor)

        # Si hay menos de 5 recetas que cumplan con los criterios, agrega más recetas aleatorias
        if len(random_low_fat_recipes) < 5:
            # Realiza otra búsqueda aleatoria sin el filtro de baja grasa para completar la lista
            additional_recipes = list(
                self.collection.aggregate(
                    [{"$sample": {"size": 5 - len(random_low_fat_recipes)}}]
                )
            )
            random_low_fat_recipes += additional_recipes

        # Baraja aleatoriamente la lista de recetas antes de devolverla
        return sample(random_low_fat_recipes, len(random_low_fat_recipes))
