import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
whatsapp_from = os.getenv('TWILIO_WHATSAPP_NUMBER')
whatsapp_to = os.getenv('DESTINATARIO_WHATSAPP')

client = Client(account_sid, auth_token)

def enviar_mensagem_whatsapp(mensagem, destino=whatsapp_to):
    try:
        message = client.messages.create(
            from_=whatsapp_from,
            body=mensagem,
            to=destino
        )
        print(f"✅ Mensagem enviada com sucesso! SID: {message.sid}")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

