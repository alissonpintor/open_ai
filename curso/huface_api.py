import dotenv
import os
import requests as rq

dotenv.load_dotenv()

# 'https://huggingface.co/inference-endpoints/'
# 'https://api-inference.huggingface.co/models/'
token = os.environ['TOKEN_HF']
inference_token = 'Bearer {token}'
headers = {"Authorization": inference_token}

modelo = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
modelo_meta = 'meta-llama/Meta-Llama-3.1-8B-Instruct'
url = f'https://api-inference.huggingface.co/models/{modelo_meta}'
json = {
    'inputs': 'Hello, what is your name?'
}

response = rq.post(url, headers=headers, json=json)
print(response)
print(response.json())