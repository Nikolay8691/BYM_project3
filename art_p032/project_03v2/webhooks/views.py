from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.utils import process_telegram_message, process_telegram_message_ok
# from chat.tasks import send_telegram_reply

# Create your views here.

class TelegramWebhook(APIView):
	
	def post(self, request, token):
		if token != settings.TELEGRAM_WEBHOOK_TOKEN:
			return Response(
				{"error": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
				)

		try:
			print('\n request.data (TelegramWebhook_view) :')
			print(request.data)
			process_telegram_message(request.data)
			# send_telegram_reply.delay(request.data)

		except KeyError:
			print('\n request.data (TelegramWebhook_view) : KeyError raised ')
			process_telegram_message_ok(request.data)

		except Exception as err:
			print('\n request.data (TelegramWebhook_view) -> Error : ', str(err))
			process_telegram_message_ok(request.data)

		finally:
			return Response({"success": True})

	# def post(self, request):
	# 	print(request.data)
	# 	return Response({'success': True})