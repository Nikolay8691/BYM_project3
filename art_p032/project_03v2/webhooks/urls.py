from django.urls import path
from . import views

app_name = 'webhooks'
urlpatterns = [
    # path('telegram/<str:token>/', views.TelegramWebhook.as_view(), name='telegram_webhook'),
    path('telegram/', views.TelegramWebhook.as_view(), name='telegram_webhook'),
]