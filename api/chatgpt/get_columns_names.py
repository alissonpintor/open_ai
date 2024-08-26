import json
from api.chatgpt.client import ChatGPTClient

class GetColumnsNamesService:
    _client = None
    _prompt_messages: list = []
    _system_message = {
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

    def __init__(self) -> None:
        self._client = ChatGPTClient.instance()
    
    def execute(self, image: bytes) -> list:
        self._prompt_messages.append(self._system_message)
        user_message = self._get_user_message(image)
        self._prompt_messages.append(user_message)
        
        response = self._client.chat.completions.create(
            messages=self._prompt_messages,
            model='gpt-4o',
            response_format={
                'type': 'json_object'
            }
        )

        column_names = json.loads(response.choices[0].message.content)

        return column_names

    def _get_user_message(self, image: bytes) -> dict:
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