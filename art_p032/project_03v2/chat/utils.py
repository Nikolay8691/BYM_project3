from pprint import pprint
import requests
import json

from django.conf import settings

from .models import TelegramMessage

from .translate import get_translation

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def process_telegram_message(message):

	pprint(message)
	data_s = ''

	if 'callback_query' in message:

		reply = f"welcome to callback_query :\n type smth."
		chat_id = message["callback_query"]["message"]["chat"]["id"]

	else :

		name = message["message"]["from"]["first_name"]
		text = message["message"]["text"]
		chat_id = message["message"]["chat"]["id"]

		if '/' in text:

			reply = f"welcome to {text.lstrip('/')} :\n type the word you want to know"

		else:

			TelegramMessage.objects.create(name = name, message = text, chat_id = chat_id)

			words = text.split(' ')
			language = words[0].lower().rstrip(':')
			languages_choices = {
									'es' : 'espana', 
									'fr' : 'ranska', 
									'it' : 'italia', 
									'de' : 'saksa', 
									'fi' : 'suomi', 
									'ru' : 'venäjä', 
									'ko' : 'korea'
								}

			if len(words) > 1 and (language in languages_choices):
				to_translate = ' '.join(words[1:])
				sentence = (languages_choices[language], to_translate)
				reply = get_translation(sentence)

			else:
				reply = 'Invalid command. Send like - de girl - to translate girl to german'

			# reply = f"hei {name}! Oon saannut viestasi {text}"

			keyboard_array = [
				[
					{'text' : 'option_1', 'callback_data' : 'right'},
					{'text' : 'option_2', 'callback_data' : 'left'}
				],
				[
					{'text' : 'option_3', 'callback_data' : 'up'}
				]
			]

			reply_markup_dict = {'inline_keyboard' : keyboard_array}
			reply_markup_json = json.dumps({'inline_keyboard' : keyboard_array}, separators=(',', ':'))

			# print('reply_markup.inline_keyboard / type : ', type(reply_markup))
			# pprint(reply_markup.inline_keyboard)

			data_s = {"chat_id": chat_id, "text": reply, "reply_markup" : reply_markup_json}

			# print('\n data :')
			# pprint(data)

			# print('\n data_s :')
			# pprint(data_s)

	data = {"chat_id": chat_id, "text": reply}

	reply_url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"

	if data_s:
		r = requests.post(reply_url, data = data_s)
	else:
		r = requests.post(reply_url, data = data)
	

	print(' Response : (utils.py) ', type(r))
	print(r.json())