import requests
import os

ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
TO_PHONE_NUMBER = os.getenv("WHATSAPP_TO_PHONE_NUMBER")  # no formato internacional sem sinais, ex: "5511999999999"

def enviar_mensagem_texto(mensagem):
    url = f"https://graph.facebook.com/v15.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": TO_PHONE_NUMBER,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print("Erro ao enviar mensagem:", response.text)

if __name__ == "__main__":
    enviar_mensagem_texto("Olá! Este é um teste da API oficial WhatsApp Business.")
