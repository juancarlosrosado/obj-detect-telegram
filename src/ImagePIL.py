from PIL import Image
import io
import base64


def string_to_bytes(base64_string):
    return base64.b64decode(base64_string)


def bytes_2_image(bytes_imagen):
    image = Image.open(io.BytesIO(bytes_imagen))
    return image
