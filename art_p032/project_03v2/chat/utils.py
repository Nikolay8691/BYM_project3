import requests

from django.conf import settings

from .models import TelegramMessage

from .translate import get_translation

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

	data = {"chat_id": chat_id, "text": reply}
	requests.post(reply_url, data = data)