
import io
from PIL import Image
class imagem:
    def __init__(self, image: Image.Image):
        self.image = image

    def process(self) -> bytes:
        img = self._redimensionar(self.image)
        resultado = self._comprimir(img)
        return resultado

    def _redimensionar(self, img: Image.Image) -> Image.Image:
        img = img.convert("RGB")
        img.thumbnail((1280, 720))  # mantém proporção
        return img

    def _comprimir(self, img: Image.Image) -> bytes:
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=75, optimize=True)
        buffer.seek(0)
        return buffer.getvalue()
