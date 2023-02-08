import requests

from django.conf import settings
from django.core.management import BaseCommand
from django.urls import reverse

class Command(BaseCommand):

	help = "Set new telegram webhook"

	def add_arguments(self,parser):
		parser.add_argument("root_url", type=str)

	def handle(self, *args, **options):
		root_url = options["root_url"]
		# webhook_path = reverse("webhooks:telegram_webhook", kwargs = {"token": settings.TELEGRAM_WEBHOOK_TOKEN})
		webhook_path = reverse("webhooks:telegram_webhook")

		webhook_url = f"{root_url}{webhook_path}"

		set_webhook_api = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/setWebhook"


		self.stdout.write(f"root_url : {root_url} webhook_path : {webhook_path}\n Setting webhook url {webhook_url}\n")
		requests.post(set_webhook_api, data={"url": webhook_url})