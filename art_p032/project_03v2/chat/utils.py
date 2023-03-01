from pprint import pprint
import requests
import json

from django.conf import settings

from .models import TelegramMessage

# from .translate import get_translation
from .translate import process_callbackquery, process_command, process_text_message, process_test_answer

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def process_telegram_message(message):

	print('\n process_telegram_message :')
	pprint(message)

	if 'callback_query' in message:
		data = process_callbackquery(message)

	elif '/' in message['message']['text']:
		data = process_command(message)

	elif '*' in message['message']['text']:
		data = process_test_answer(message)

	else:
		data = process_text_message(message)

	# data = {"chat_id": chat_id, "text": reply}

	reply_url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"

	r = requests.post(reply_url, data = data)

	print(' Response : (utils.py) ', type(r))
	pprint(r.json())


def process_telegram_message_ok(message):	

	print('\n process_telegram_message_ok :')
	pprint(message)

	if 'callback_query' in message:
		chat_id = message["callback_query"]["message"]["chat"]["id"]
	else:
		chat_id = message["message"]["chat"]["id"]

	reply = 'to start - use <b>Menu button</b> to choose command'
	data = {"chat_id": chat_id, "text": reply, "parse_mode" : "HTML"}

	reply_url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"

	r = requests.post(reply_url, data = data)

	print(' Response : (utils.py) ', type(r))
	pprint(r.json())
