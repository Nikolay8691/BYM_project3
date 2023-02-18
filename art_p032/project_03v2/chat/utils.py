from pprint import pprint
import requests
import json

from django.conf import settings

from .models import TelegramMessage

from .translate import get_translation

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def process_telegram_message(message):
	name = message["message"]["from"]["first_name"]
	text = message["message"]["text"]
	chat_id = message["message"]["chat"]["id"]

	TelegramMessage.objects.create(name = name, message = text, chat_id = chat_id)

	words = text.split(' ')
	language = words[0].lower()
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

	reply_url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"

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

	data = {"chat_id": chat_id, "text": reply}
	data_s = {"chat_id": chat_id, "text": reply, "reply_markup" : reply_markup_json}

	# print('\n data :')
	# pprint(data)

	# print('\n data_s :')
	# pprint(data_s)

	# r = requests.post(reply_url, data = data)
	r = requests.post(reply_url, data = data_s)

	print(' Response : (utils.py) ', type(r))
	print(r.json())