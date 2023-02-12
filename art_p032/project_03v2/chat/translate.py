import random

def get_translation(sentence):

	se = ''
	if sentence[0] == 'suomi':
		se = input(f' translate : {sentence[1]} - ')
		return f'sinä kirjoitit - {sentence[1]}. suomeksi se on {se}'

	else:
		times = random.randint(1, 10)
		return f'sinä kirjoitit - {sentence[1]}. {sentence[0]}ksi se on ... en tiedä vielä.\n just try {times} times more and you will know!'