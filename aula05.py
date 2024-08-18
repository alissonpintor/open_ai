import openai
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
client = openai.Client()

def gerar_texto(mensagens: list, model='gpt-3.5-turbo-0125', max_tokens=1000, temperature=0, stream=False):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream
    )

    texto_resposta = ''

    print('Assistant: ', end='')

    if stream:
        for stream_resposta in resposta:
            texto = stream_resposta.choices[0].delta.content
            if texto:
                print(texto, end='')
                texto_resposta += texto
    else:
        print(resposta.choices[0].message.content)
        texto_resposta = resposta.choices[0].message.content
    print()
        
    # mensagens.append(resposta.choices[0].message.model_dump(exclude_none=True))
    mensagens.append({
        'role': 'assistant',
        'content': texto_resposta
    })

    return mensagens

if __name__ == '__main__':
    mensagens = []
    print('Bem vindo ao chatBot ++++++++++++')
    
    while True:
        pergunta = input('User: ')
        mensagens.append({'role': 'user', 'content': pergunta})
        gerar_texto(mensagens=mensagens, stream=True)
