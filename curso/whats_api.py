# https://pywa.readthedocs.io/en/latest/content/getting-started.html
# https://developers.facebook.com/
# https://business.facebook.com/


import os
from pywa import WhatsApp
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

phone_id = os.environ.get('WHATSAPP_API_PHONE_ID')
token = os.environ.get('WHATSAPP_API_TOKEN')

if token:
    wp = WhatsApp(phone_id=phone_id, token=token)

    message = wp.send_message(
        to='5565999976012',
        text='Primeiro teste de envio de mensagem'
    )
    print(message)