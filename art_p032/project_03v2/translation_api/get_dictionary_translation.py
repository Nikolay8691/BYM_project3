import requests

from pprint import pprint

def get_google(word, language_code):

	url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

	# payload = "q=Hello%2C%20world!&target=es&source=en"
	payload = 'q=' + word + '&target=' + language_code

	headers = {
		"content-type": "application/x-www-form-urlencoded",
			"Accept-Encoding": "application/gzip",	
			"X-RapidAPI-Key": "dae7acf879msh176ee67d0486e61p14b9a5jsn344207c6c0fd",	
			"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
			}

	# # response = requests.request("POST", url, data=payload, headers=headers)
	# response_2 = requests.post(url, data=payload, headers=headers)
	# print('response_2 type : ', type(response_2))

	# # print('response_2.text : ', response_2.text)
	# # print('response_2.text type : ', type(response_2.text))

	# r = response_2.json()
	# print('response_2.json type : ', type(r))
	# pprint(r)

	# return r['data']['translations'][0]['translatedText']
	return f'Okay'
