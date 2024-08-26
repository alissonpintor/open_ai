import base64
from io import BytesIO
from pdf2image import convert_from_bytes
from PIL import Image


class PdfFileHandler:
    def process_pdf_to_image(self, pdf_file: bytes) -> list[bytes]:
        images: list = self.__convert_pdf_to_image(pdf_file)
        images_base64: list = []

        if images:
            for image in images:
                base64_image: bytes = self.__convert_image_to_base64(image)
                images_base64.append(base64_image)

        return images_base64
    
    def __convert_pdf_to_image(self, pdf_file: bytes) -> list:
        try:
            images: list = convert_from_bytes(pdf_file) 
            return images
        except:
            raise Exception('Erro ao converter o pdf para imagem')

    def __convert_image_to_base64(self, image: bytes) -> bytes:
        try:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image_bytes = buffered.getvalue()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            return image_base64
        except:
            raise Exception('Erro ao converter a imagem para Base64')