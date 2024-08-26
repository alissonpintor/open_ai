import streamlit as st
import dotenv
import json
import openai
import base64
from io import BytesIO
from pdf2image import convert_from_path, convert_from_bytes


dotenv.load_dotenv()
client = openai.Client()

# images = convert_from_path('arquivos/pedido_renner.pdf')
# for index, image in enumerate(images):
#     image.save(f'arquivos/renner_page{index}.jpg', 'JPEG')

def convert_pdf_to_image(pdf_file_bytes, name: str):
    images = convert_from_bytes(pdf_file_bytes) 
    return images     

def convert_image_to_base64(image) -> bytes:
    #image.save(f'arquivos/{name}_page{index}.jpg', 'JPEG')
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return image_base64

def get_column_names(document_image):
    pass

if __name__ == '__main__':
    prompt_messages: list = []
    images: list = []
    base64_images: list = []
    
    image_name = st.text_input('Informe um nome para as imagens geradas')
    pdf_file_uploaded = st.file_uploader('Selecione o pdf a ser convertido', 'pdf')
    
    if pdf_file_uploaded and image_name:
        print('Convertendo imagens...')
        images = convert_pdf_to_image(pdf_file_uploaded.getvalue(), image_name)
    
    if images:
        print('Convertendo para Base64...')
        for image in images:
            base64_image = convert_image_to_base64(image)
            base64_images.append(base64_image)
    
    if base64_images:
        print('Enviando para o ChatGPT...')
        
        system_message = {
            'role': 'assistant',
            'content': '''
                Você recebe uma imagem que possui textos com uma tabela de itens e deve retornar o um json contendo 
                o nome dessas tabelas seguindo um exemplo a seguir entre ####:

                ####
                {
                    "colunas": ["Produto", "Descrição", "Emb.", "Qtdade", "Vlr.Unit"]
                }
                ####

                Retorne somente o json na resposta
            '''
        }
        prompt_messages.append(system_message)

        page01_image = {
            'role': 'user',
            'content': [
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': f'data:image/jpeg;base64,{base64_images[0]}'
                    }
                }
            ]
        }
        prompt_messages.append(page01_image)
        
        response = client.chat.completions.create(
            messages=prompt_messages,
            model='gpt-4o',
            response_format={
                'type': 'json_object'
            }
        )

        column_names = json.loads(response.choices[0].message.content)

        if column_names:
            st.selectbox('Colunas', column_names['colunas'])
    