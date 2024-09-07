import json

from openai import Client
from openai.types.chat.chat_completion import ChatCompletion
from api.chatgpt.client import ChatGPTClient

antigo = {
            'role': 'assistant',
            'content': '''
                Você recebe uma imagem de um pedido de venda contendo uma tabela de itens e deve retornar um json contendo 
                o nome das colunas dessa tabela seguindo um exemplo a seguir entre ####:

                ####
                {
                    "colunas": ["Produto", "Descrição", "Emb.", "Qtdade", "Vlr.Unit"]
                }
                ####

                Retorne somente o json na resposta  não invete valores que não existem
            '''
        }


class GetColumnsNamesService:

    def __init__(self) -> None:
        self.__client: Client = ChatGPTClient.instance()
        self.__prompt_messages: list = []

    def execute(self, image: str) -> list:
        self.__prompt_messages.append(self.__get_system_message())
        user_message = self.__get_user_message(image)
        self.__prompt_messages.append(user_message)

        response: ChatCompletion = self.__client.chat.completions.create(
            messages=self.__prompt_messages,
            model='gpt-4o',
            temperature=0,
            response_format={
                'type': 'json_object'
            }
        )

        if response.choices[0].message.content is None:
            return []

        json_response = json.loads(response.choices[0].message.content)
        column_names: list = json_response.get('colunas', [])

        return column_names

    def __get_system_message(self) -> dict[str, str]:
        return {
            'role': 'assistant',
            'content': '''
                Você recebe uma imagem de um pedido de venda contendo uma tabela de itens e deve extrair os
                nomes das colunas dessa tabela. Retorne um json com os nomes dessas colunas e não invente
                valores que não existem na imagem.
            '''
        }

    def __get_user_message(self, image: str) -> dict:
        return {
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
