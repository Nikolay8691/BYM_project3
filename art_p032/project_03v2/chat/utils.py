import requests

from django.conf import settings

from .models import TelegramMessage

def process_telegram_message(message):
	name = message["message"]["from"]["first_name"]
	text = message["message"]["text"]
	chat_id = message["message"]["chat"]["id"]

	TelegramMessage.objects.create(name = name, message = text, chat_id = chat_id)

	reply = f"hei {name}! Oon saannut viestasi {text}"

	reply_url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"

	data = {"chat_id": chat_id, "text": reply}
	requests.post(reply_url, data = data)