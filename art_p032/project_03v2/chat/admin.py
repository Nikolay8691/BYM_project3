from django.contrib import admin

from .models import TelegramMessage, NewWords, Tests, TestResult
# Register your models here.

@admin.register(TelegramMessage)
class TelegramMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'chat_id')

admin.site.register(NewWords)
admin.site.register(Tests)
admin.site.register(TestResult)