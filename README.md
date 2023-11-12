# obj-detect-telegram

Este es un ChatBot de Telegram que te permite enviar una foto de ingredientes y, utilizando la detección de objetos en imágenes, identificar los ingredientes presentes en la imagen. Una vez que se han identificado los ingredientes, el ChatBot buscará recetas que incluyan esos ingredientes y te proporcionará una lista de recetas que puedes preparar con lo que tienes.

## Requisitos

Para utilizar este ChatBot de Telegram, necesitarás:

- Una cuenta de Telegram.

- Acceso al bot de Telegram que se encuentra en este enlace: [enlace del chatbot](https://t.me/IMF_TFM_BOT)

## Instrucciones de Uso

1. **Iniciar el ChatBot**. Busca el ChatBot de Telegram por su nombre de usuario: @TestPredictionBot y ábrelo.

2. **Enviar una foto**. Utiliza la función de enviar fotos de Telegram para enviar una imagen que contenga los ingredientes que quieres identificar. Asegúrate de que los ingredientes estén claramente visibles en la foto.

3. **Esperar la respuesta**. El ChatBot procesará la imagen y tratará de identificar los ingredientes presentes en la misma.

4. **Recibir recetas**. Una vez que los ingredientes se hayan identificado correctamente, el ChatBot buscará recetas que incluyan esos ingredientes y te proporcionará una lista de recetas que puedes preparar con lo que tienes. Selecciona una receta para obtener los detalles y las instrucciones de preparación.

## Tecnología Utilizada

Este ChatBot de Telegram utiliza una variedad de tecnologías para ofrecer sus funciones, incluyendo:

- **Detección de objetos en imágenes**: se utiliza un modelo de detección de objetos entrenado basado en YOLOv8 para identificar los ingredientes presentes en las imágenes. El codigo se encuentra en el siguiente repositorio [enlace al repositorio de YOLO](https://github.com/juancarlosrosado/obj-detect-yolo).

- **Búsqueda de recetas**: se integra con una base de datos de recetas en MongoDB para buscar recetas que incluyan los ingredientes detectados.

- **Interfaz de Telegram**: utiliza la API de Telegram para interactuar con los usuarios y enviar y recibir mensajes y fotos.

## Variables de entorno

Para poder correr este script es necesario las siguientes variables de entorno:

- `TELEGRAM_TOKEN`: Token del chatbot de Telegram

- `MONGO_URI`: URI de MongoDB

- `FOTOS_DIR`: directorio donde guardar las imagenes que envíen los usuarios

- `API_YOLO`: URL para llamar a la API de YOLO

## Limitaciones

Es importante tener en cuenta algunas limitaciones de este ChatBot:

- La precisión de la detección de ingredientes en las imágenes puede variar dependiendo de la calidad de la foto y la visibilidad de los ingredientes.

- La base de datos de recetas puede no contener todas las posibles recetas que incluyan los ingredientes detectados.

- Este ChatBot funciona mejor con ingredientes comunes y fáciles de reconocer.
