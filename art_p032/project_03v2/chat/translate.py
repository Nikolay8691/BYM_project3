import random

import json

from .models import TelegramMessage

languages_choose_from = {
						'es' : 'espana', 
						'fr' : 'ranska', 
						'it' : 'italia', 
						'de' : 'saksa', 
						'fi' : 'suomi', 
						'ru' : 'venäjä', 
						'ko' : 'korea'
					}

# def get_translation(sentence) -> tuple:

# 	se = ''
# 	if sentence[0] == 'suomi':
# 		se = input(f' translate : {sentence[1]} - ')
# 		reply_status == True
# 		reply = f'sinä kirjoitit - {sentence[1]}. suomeksi se on {se}'

# 	else:
# 		times = random.randint(1, 10)
# 		reply_status = not(times == 1)
# 		reply = f'sinä kirjoitit - {sentence[1]}. {sentence[0]}ksi se on ... en tiedä vielä.\n just try {times} times more and you will know!'

# 	return (reply, reply_status)

def get_translation(sentence) -> dict:

	reply = {}
	# se = ''
	if sentence[0] == 'suomi':
		se = input(f' translate : {sentence[1]} - ')
		reply['status'] = True
		reply['text'] = f'sinä kirjoitit - {sentence[1]}. suomeksi se on {se}'

	else:
		se = 'no_translation'
		times = random.randint(1, 10)
		reply['status'] = not(times == 1)
		reply['text'] = f'sinä kirjoitit - {sentence[1]}. {sentence[0]}ksi se on ... en tiedä vielä.\n just try {times} times more and you will know!'

	reply['word_original'] = sentence[1]
	reply['word_translation'] = se

	return reply


def process_callbackquery(message):

	message_body = message["callback_query"]["message"]
	chat_id = message_body["chat"]["id"]
	word = message_body["text"]

	word_and_translation = message_body["reply_markup"]["inline_keyboard"][0][0]["callback_data"]
	
	words = word_and_translation.split(':')
	word_original = words[0]
	word_translation = words[1]

	reply = f"Okay, {word_original} with {word_translation} is in FDB now"
	
	return {"chat_id": chat_id, "text": reply}


def process_command(message):

	text = message["message"]["text"]
	chat_id = message["message"]["chat"]["id"]

	if text == "/newwords":
		languages = ",\n".join(f'   {code} : {language}' for code, language in sorted(languages_choose_from.items()))
		languages_list_title = "languages to choose from "
		invitation = "\ntype the word you want to know, like\nlanguage_code: new_word (ex. de: hello)"
		reply = f"{languages_list_title} :\n{languages}\nwelcome to '{text.lstrip('/')}' study : {invitation}"

	elif text == "/newtest":
		reply = f"welcome to {text.lstrip('/')} exercise :\n its' logic is not ready yet. "

	else:
		reply = f"Smth. is wrong, check your inputs!"

	return {"chat_id": chat_id, "text": reply}


def process_text_message(message):

	name = message["message"]["from"]["first_name"]
	text = message["message"]["text"]
	chat_id = message["message"]["chat"]["id"]

	words = text.split(' ')
	language = words[0].lower().rstrip(':')

	if len(words) > 1 and (language in languages_choose_from):

		to_translate = ' '.join(words[1:])
		sentence = (languages_choose_from[language], to_translate)
		# reply, reply_status = get_translation(sentence)
		reply_dict = get_translation(sentence)
		# reply_status = reply_dict['status']
		# reply_text = reply_dict['text']
		# reply = json.dumps(reply_dict)

		# if reply_status:
		if reply_dict['status']:
			TelegramMessage.objects.create(name = name, message = text, chat_id = chat_id)

			callback_data = f"{reply_dict['word_original']}:{reply_dict['word_translation']}"
			keyboard_array = [[{'text' : ' += FDB (store in _my favorites_ database)', 'callback_data' : callback_data}]]
			reply_markup_json = json.dumps({'inline_keyboard' : keyboard_array}, separators=(',', ':'))

			# return {"chat_id": chat_id, "text": reply_text, "reply_markup" : reply_markup_json}
			return {"chat_id": chat_id, "text": reply_dict["text"], "reply_markup" : reply_markup_json}

		else:

			reply = 'Strange - nobody knows this word but you. \nSend it to Oxford : oxford-new@gmail.com\n they will check it out!'
			return {"chat_id": chat_id, "text": reply}

	else:
		reply = 'Invalid command - check the message and/or language code. Send like - de: girl - to translate girl to german'
		return {"chat_id": chat_id, "text": reply}

	# reply = f"hei {name}! Oon saannut viestasi {text}"
