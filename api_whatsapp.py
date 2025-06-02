# api_whatsapp.py

import os
from twilio.rest import Client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Variáveis sensíveis carregadas de forma segura
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_ACCOUNT_SID')
whatsapp_from = os.getenv('whatsapp:+14155238886')  
default_destino = os.getenv('whatsapp:+5511964326385')  

# Cria o cliente Twilio
client = Client(account_sid, auth_token)

def enviar_mensagem_whatsapp(mensagem, destino=default_destino):
    """
    Envia uma mensagem de alerta via WhatsApp utilizando Twilio.

    Parâmetros:
    - mensagem (str): Texto da mensagem a ser enviada
    - destino (str): Número de telefone destino no formato 'whatsapp:+55...'
    """
    if not all([account_sid, auth_token, whatsapp_from, destino]):
        print("❌ Erro: Variáveis de ambiente ausentes ou mal configuradas.")
        return

    try:
        message = client.messages.create(
            from_=whatsapp_from,
            body=mensagem,
            to=destino
        )
        print(f"✅ Alerta enviado via WhatsApp! SID da mensagem: {message.sid}")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem via WhatsApp: {e}")
