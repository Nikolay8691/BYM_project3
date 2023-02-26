import random

import json

from pprint import pprint

from .models import TelegramMessage, NewWords, Tests, TestResult

from translation_api.get_dictionary_translation import get_google

languages_choose_from = {
						'es' : 'espana', 
						'fr' : 'ranska', 
						'it' : 'italia', 
						'de' : 'saksa', 
						'fi' : 'suomi', 
						'ru' : 'venäjä', 
						'ko' : 'korea'
					}

test_id = 0
test_result_id = 0

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
	if sentence[0] == 'fi':
		se = input(f' translate : {sentence[1]} - ')
		# se = get_google(sentence[1], 'fi')
		reply['status'] = True
		reply['text'] = f'sinä kirjoitit - {sentence[1]}. suomeksi se on {se}'

	else:
		se = 'no_translation'
		times = random.randint(1, 10)
		reply['status'] = not(times == 1)
		reply['text'] = f'sinä kirjoitit - {sentence[1]}. {languages_choose_from[sentence[0]]}ksi se on ... en tiedä vielä.\n just try {times} times more and you will know!'

	reply['word_original'] = sentence[1]
	reply['word_translation'] = se
	reply['source_language'] = 'en'
	reply['target_language'] = sentence[0]

	return reply

# def process_test_question(test_id):
def process_test_question():

	global test_id
	global test_result_id
	# test_id = request.session['test_id']

	test = Tests.objects.get(pk = test_id)
	direction = test.direction
	user_words = NewWords.objects.filter(user = test.user)
	user_language_words = user_words.filter(target_language = test.target_language)
	print(' direction : ', direction, ' language : ', test.target_language)
	word_data = random.choice(user_language_words)

	test_result = TestResult(test = test, word = word_data, tries = 0, status = False)
	test_result.save()
	
	test_result_id = test_result.id
	# request.session['test_result_id'] = test_result.id

	print(' process_test_question : ')
	print(' test_id : ', test_id)
	print(' test_result_id : ', test_result_id)

	if direction == 'forward':			
		question = f"{word_data.word_original} - ?({languages_choose_from[word_data.target_language]}ksi)\nStart your answer with '*', like *hello"

	elif direction == 'backward':
		question = f"{word_data.word_translation} - ?(englanniksi)\nStart your answer with '*', like *hello"

	else:
		question = f"Smth. is wrong with direction"

	return question

def process_test_answer(message):

	global test_id
	global test_result_id
	# test_id = request.session['test_id']
	# test_result_id = request.session['test_result_id']

	test = Tests.objects.get(pk = test_id)
	direction = test.direction

	test_result = TestResult.objects.get(pk = test_result_id)
	test_word = test_result.word

	if direction == 'forward':
		word_questioned = test_word.word_original
		language = languages_choose_from[test_word.target_language]
		right_answer = test_word.word_translation
	else:
		word_questioned = test_word.word_translation
		language = 'englanni'
		right_answer = test_word.word_original

	text = message["message"]["text"]
	chat_id = message["message"]["chat"]["id"]
	word_answer = text.lstrip('*')

	test_result.tries += 1
	keyboard_array =[]

	if word_answer == right_answer:
		test_result.status = True
		answer = 'correct. congratulations'

	elif test_result.tries < 2:
		# test_result.tries += 1
		# test_result.status = False
		answer = 'mistake. you can try 1 more time'
		callback_data = f'test_repeat:{direction}:{language}:{word_questioned}'
		keyboard_row = [{'text' : ' Try 1 more time ', 'callback_data' : callback_data}]
		keyboard_array.append(keyboard_row)

	else:
		# test_result.status = False
		answer = f'mistake. right_answer = {right_answer} '

	test_result.save()

	keyboard_row = [
					{'text' : ' next word', 'callback_data' : 'test_next_word:'},
					{'text' : ' stop test ', 'callback_data' : 'test_stop'}
					]
	keyboard_array.append(keyboard_row)

	reply_text = answer
	reply_markup_json = json.dumps({'inline_keyboard' : keyboard_array}, separators=(',', ':'))

	return {"chat_id": chat_id, "text": reply_text, "reply_markup" : reply_markup_json}

	# return{"chat_id": chat_id, "text": 'everything is okay'}

def process_test_results():

	global test_id
	global test_result_id
	# test_id = request.session['test_id']
	# test_result_id = request.session['test_result_id']

	test = Tests.objects.get(pk = test_id)
	test_results_all = test.test_origin.all()

	i, j, k = (0, 0, 0)
	for test_result in test_results_all:
		i += test_result.tries
		j += 1
		if test_result.status: k += 1
	
	reply_stats = f'tested dictionary consists of {test.number_of_words}\n tested {j} words in {i} tries\n correct {k}, wrong {j-k}'
	return reply_stats

def process_callbackquery(message):
	global test_id
	# if 'test_id' not in request.session:
	# 	request.session['test_id'] = 0
	# test_id = request.session['test_id']		

	message_body = message["callback_query"]["message"]
	chat_id = message_body["chat"]["id"]
	word = message_body["text"]

	print(' callback_query : ', type(message['callback_query']))
	pprint(message['callback_query'])
	user_id = str(message["callback_query"]["from"]["id"])
	user_first_name = message["callback_query"]["from"]["first_name"]

	process, *data = message["callback_query"]["data"].split(':')
	# print(' data : ')
	# print(data)
	# print('process : ', process)

	if process == 'text_message':
		# store in FDB

		source_language, word_original, target_language, word_translation = data
		f = NewWords(
					source_language = source_language, 
					word_original = word_original, 
					target_language = target_language, 
					word_translation = word_translation, 
					user = user_id,
					user_first_name = user_first_name
					)
		f.save()

		reply = f"Okay, {word_original} with {word_translation} is in FDB now"
		return {"chat_id": chat_id, "text": reply}

	elif process == 'test_repeat':
		# test - 2nd try
		direction, language, word_questioned = data
		question = f"{word_questioned} - ?({language}ksi)\nStart your answer with '*', like *hello\nLast try!"

		return {"chat_id": chat_id, "text": question}

	elif process == 'test_next_word':
		question = process_test_question()
		return {"chat_id": chat_id, "text": question}

	elif process == 'test_stop':
		test_result_stats = process_test_results()
		return {"chat_id": chat_id, "text": test_result_stats}

	else:
		# command - /newtest, process == 'test', after test type button's pressed 

		direction, language, number = data
		test = Tests(
						user = user_id, 
						user_first_name = user_first_name, 
						direction = direction,
						target_language = language,
						number_of_words = number
					)
		test.save()
		# question = process_test_question(test.id)
		test_id = test.id
		# request.session['test_id'] = test.id

		question = process_test_question()

		return {"chat_id": chat_id, "text": question}


def process_command(message):

	text = message["message"]["text"]
	chat_id = message["message"]["chat"]["id"]

	if text == "/start":
		reply = "welcome to translation_BOT! choose any command from the menu button to start working."
		return {"chat_id": chat_id, "text": reply}

	elif text == "/newwords":
		languages = ",\n".join(f'   {code} : {language}' for code, language in sorted(languages_choose_from.items()))
		languages_list_title = "languages to choose from "
		invitation = "\ntype the word you want to know, like\nlanguage_code: new_word (ex. de: hello)"
		reply = f"{languages_list_title} :\n{languages}\nwelcome to '{text.lstrip('/')}' study : {invitation}"
		return {"chat_id": chat_id, "text": reply}

	elif text == "/newtest":

		print(' message = command : ', type(message['message']))
		print(message['message'])

		user_id = message["message"]["from"]["id"]
		user_first_name = message["message"]["from"]["first_name"]

		user_words = NewWords.objects.filter(user = user_id)

		user_dict = {}
		n = 0		
		for word in user_words:
			language = word.target_language
			if language not in user_dict:
				n += 1
				user_dict[language] = 1
			else:
				user_dict[language] += 1

		# reply_text = f"welcome to {text.lstrip('/')} exercise :\n you study {n} language(s) - choose test button"
		# reply = f"welcome to {text.lstrip('/')} exercise :\n its' logic is not ready yet. "

		if n > 0:
			keyboard_array = []
			for language, number in user_dict.items():
				callback_data_forward = f'test:forward:{language}:{number}'
				callback_data_back = f'test:backward:{language}:{number}'
				keyboard_row = [
					{
					# 'text' : f'from english => \nto {languages_choose_from[language]}\n {number} word(s)',
					'text' : f'en => {language}\n{number} word(s)',
					'callback_data' : callback_data_forward
					}, 
					{
					# 'text' : f'<= from {languages_choose_from[language]}\n to english \n{number} word(s)',
					'text' : f'en <= {language}\n{number} word(s)', 
					'callback_data' : callback_data_back
					} 
								]
				keyboard_array.append(keyboard_row)

			reply_text = f"welcome to {text.lstrip('/')} exercise :\n you study {n} language(s) - choose test button"
			reply_markup_json = json.dumps({'inline_keyboard' : keyboard_array}, separators=(',', ':'))

			print(reply_text)
			print(' reply_markup_json = command : ')
			pprint(reply_markup_json)

			return {"chat_id": chat_id, "text": reply_text, "reply_markup" : reply_markup_json}
			# reply = f'I am glad you are here'

		else:
			reply = f'you do not study any language yet.\n /newwords is the right choice for you'
			return {"chat_id": chat_id, "text": reply}

	else:
		reply = f"Smth. is wrong, check your inputs!"
		return {"chat_id": chat_id, "text": reply}

	return {"chat_id": chat_id, "text": reply}


def process_text_message(message):

	name = message["message"]["from"]["first_name"]
	text = message["message"]["text"]
	chat_id = message["message"]["chat"]["id"]

	words = text.split(' ')
	language = words[0].lower().rstrip(':')

	if len(words) > 1 and (language in languages_choose_from):

		word_to_translate = ' '.join(words[1:])
		sentence = (language, word_to_translate)

		# reply, reply_status = get_translation(sentence)
		reply_dict = get_translation(sentence)

		# if reply_status:
		if reply_dict['status']:
			TelegramMessage.objects.create(name = name, message = text, chat_id = chat_id)

			callback_data = f"text_message:{reply_dict['source_language']}:{reply_dict['word_original']}:{reply_dict['target_language']}:{reply_dict['word_translation']}"
			keyboard_array = [[{'text' : ' += FDB (store in _my favorites_ database)', 'callback_data' : callback_data}]]
			reply_markup_json = json.dumps({'inline_keyboard' : keyboard_array}, separators=(',', ':'))

			# return {"chat_id": chat_id, "text": reply_text, "reply_markup" : reply_markup_json}
			return {"chat_id": chat_id, "text": reply_dict["text"], "reply_markup" : reply_markup_json}

		else:

			reply = 'Strange - nobody knows this word but you. \nSend it to Oxford : oxford-new@gmail.com\n they will check it out!'
			return {"chat_id": chat_id, "text": reply}

	else:
		reply = 'Invalid command - check the message inputs :\nfor newwords send like - de: girl - to translate girl to german\nfor test send like - *word_answer - to compare with right_answer'
		# reply = 'Invalid command - check the message and/or language code. Send like - de: girl - to translate girl to german'
		return {"chat_id": chat_id, "text": reply}

	# reply = f"hei {name}! Oon saannut viestasi {text}"
