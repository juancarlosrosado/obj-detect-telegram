import os
from dotenv import load_dotenv
import datetime
import json
import cv2
from ultralytics import YOLO


class ModeloYOLO:
    def __init__(self, image_path, id):
        self.image_path = image_path
        self.id = id
        load_dotenv()

    def predict(self):
        """
        Realiza una predicción sobre una imagen
        """
        try:
            WEIGHTS_PATH = os.getenv("WEIGHTS_PATH")

            source = cv2.imread(self.image_path)
            datetime_cet = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            model = YOLO(WEIGHTS_PATH)
            results = model.predict(
                source=source,
                save=True,
                project="predictions",
                name=self.id,
                exist_ok=True,
            )

            for result in results:
                detection_count = result.boxes.shape[0]

                for i in range(detection_count):
                    cls = int(result.boxes.cls[i].item())
                    name = result.names[cls]
                    confidence = float(result.boxes.conf[i].item())
                    obj = {
                        "id": self.id,
                        "datetime": datetime_cet,
                        "name": name,
                        "probability": round(confidence, 4),
                    }

                    with open(
                        f'predictions/{self.id}/{obj["id"]}.json', "a"
                    ) as json_file:
                        json.dump(obj, json_file, indent=4)

            return print("Done")

        except Exception as e:
            print(f"Error: {e}")
            return print("Error")
