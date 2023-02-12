from django.contrib import admin

from .models import TelegramMessage

# Register your models here.

@admin.register(TelegramMessage)
class TelegramMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'chat_id')

