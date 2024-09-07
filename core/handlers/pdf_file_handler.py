import base64
from io import BytesIO
from typing import List
from pdf2image import convert_from_bytes
import PIL.Image as img


class PdfFileHandler:
    def process_pdf_to_image(self, pdf_file: bytes) -> str | None:
        new_image: img.Image | None = None
        images: list = self.__convert_pdf_to_image(pdf_file=pdf_file)
        images_base64: list[str] = []
        base64_image: str | None = None

        if images:
            for image in images:
                new_image = image if new_image is None else self.concat_images_vertical(new_image, image)
            
            if new_image is not None:
                base64_image = self.__convert_image_to_base64(image=new_image)

        return base64_image
    
    def process_to_image(self, pdf_file: bytes) -> img.Image | None:
        new_image: img.Image | None = None
        images: list = self.__convert_pdf_to_image(pdf_file=pdf_file)

        if images:
            for image in images:
                new_image = image if new_image is None else self.concat_images_vertical(new_image, image)
            
        return new_image
    
    def convert_to_base64(self, image: img.Image) -> str:
        try:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image_bytes = buffered.getvalue()
            image_base64: str = base64.b64encode(image_bytes).decode('utf-8')
            return image_base64
        except:
            raise Exception('Erro ao converter a imagem para Base64')
    
    def __convert_pdf_to_image(self, pdf_file: bytes) -> list[img.Image]:
        try:
            images: List[img.Image] = convert_from_bytes(pdf_file=pdf_file)
            return images
        except:
            raise Exception('Erro ao converter o pdf para imagem')
    
    def concat_images_vertical(self, first_image: img.Image, second_image: img.Image) -> img.Image:
        width: int = first_image.width
        height: int = first_image.height + second_image.height        
        new_image: img.Image = img.new(
            mode='RGB',
            size=(width, height)
        )
        new_image.paste(im=first_image, box=(0, 0))
        new_image.paste(im=second_image, box=(0, first_image.height))
        return new_image

    def __convert_image_to_base64(self, image: img.Image) -> str:
        try:
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image_bytes = buffered.getvalue()
            image_base64: str = base64.b64encode(image_bytes).decode('utf-8')
            return image_base64
        except:
            raise Exception('Erro ao converter a imagem para Base64')