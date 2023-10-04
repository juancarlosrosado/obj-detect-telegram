import os
from dotenv import load_dotenv
from pymongo import MongoClient
import json

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
        Busca recetas por ingredientes en la base de datos MongoDB.

        Args:
            ingredient_list (list): Lista de ingredientes a buscar.

        Returns:
            pymongo.cursor.Cursor: Un cursor con los resultados de la búsqueda.
        """
        return self.collection.find({"categories": {"$in": ingredient_list}}).limit(5)
