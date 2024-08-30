import json
import openai
from api.chatgpt.client import ChatGPTClient
from core.models.columns import Columns
from core.models.files import Files
from typing import Any


class GetItensDataService:
    __client: openai.Client
    __prompt_messages: list = []

    def __init__(self) -> None:
        self.__client = ChatGPTClient.instance()

    def execute(self, columns: Columns, images: Files) -> None | dict[str, Any]:
        if not self.__prompt_messages:
            self.__prompt_messages.append(self.__get_system_message(columns))
        itens: dict[str, Any] = {}
        itens['columns'] = []
        itens['itens'] = []

        for image in images:
            user_message = self.__get_user_message(image)
            self.__prompt_messages.append(user_message)

            response = self.__client.chat.completions.create(
                messages=self.__prompt_messages,
                model='gpt-4o',
                response_format={
                    'type': 'json_object'
                },
                max_tokens=4000
            )

            if response.choices[0].message.content is None:
                return None
            json_response = json.loads(response.choices[0].message.content)
            item: list = json_response.get('itens')            
            itens['itens'] = item

        return itens

    def __get_system_message(self, columns: Columns) -> dict[str, str]:
        return {
            'role': 'assistant',
            'content': '''
                Você recebe uma imagem que possui textos com uma tabela de itens e deve retornar o um json contendo 
                os itens dessa tabela seguindo o exemplo entre ####:

                ####
                {
                    "itens": [
                        {
                            "Referencia": "50300201",
                            "Descrição": "DIATEX PINTA MAIS BRANCO NEVE 3,6L",
                            "Qtde": "48",
                            "Preço Líq": "24,59"                        },
                        {
                            "Referencia": "11100104",
                            "Descrição": "SELADORA CONCENTRADAINCOLOR 900 ML",
                            "Qtde": "60",
                            "Preço Líq": "16,51"
                        }
                    ]
                }
                ####
            ''' + (
            f'''
                Na imagem Referencia se chama "{columns.referencia}", Descrição se chama "{columns.descricao}",
                Qtde se chama "{columns.quantidade}" e Preço Líq se chama "{columns.vlr_unitario}". Siga os passos
                a seguir:

                1) Identifique a posição das colunas na imagem
                2) Extraia os dados referentes a cada coluna em cada linha da tabela
                3) Preenha o json com os dados extraidos de acordo com o modelo citado
                4) Passe para a próxima linha e repita os passos 2 e 3
                5) Se receber mais imagens repita os passos 1, 2, 3 e 4 e caso a tabela da imagem não possua as colunas 
                   utilize a mesma posição das colunas da primeira imagem enviada
                6) retorne o json com os dados
            '''
            )
        }
    
    def __get_user_message(self, image: bytes) -> dict:
        user_message = {
            'role': 'user',
            'content': [
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': f'data:image/jpeg;base64,{image}'
                    }
                }
            ]
        }
        return user_message