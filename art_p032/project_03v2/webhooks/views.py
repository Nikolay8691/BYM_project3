from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.utils import process_telegram_message
# from chat.tasks import send_telegram_reply

# Create your views here.

class TelegramWebhook(APIView):
	
	def post(self, request, token):
		if token != settings.TELEGRAM_WEBHOOK_TOKEN:
			return Response(
				{"error": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
				)

		print(request.data)
		process_telegram_message(request.data)
		# send_telegram_reply.delay(request.data)
		return Response({"succes": True})

	# def post(self, request):
	# 	print(request.data)
	# 	return Response({'success': True})