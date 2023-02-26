from django.db import models
# Create your models here.
class TelegramMessage(models.Model):

	name = models.CharField(max_length = 255)
	message = models.TextField()
	chat_id = models.BigIntegerField()

	def __str__(self):
		return self.name

class NewWords(models.Model):

	source_language = models.CharField(max_length = 2)
	word_original = models.CharField(max_length = 64)
	target_language = models.CharField(max_length = 2)
	word_translation = models.CharField(max_length = 64)
	user = models.CharField(max_length = 64)
	user_first_name = models.CharField(max_length = 64)

	def __str__(self):
		return f'{self.user_first_name} - {self.user}:: {self.source_language}: {self.word_original} => {self.target_language}: {self.word_translation}'

class Tests(models.Model):

	user = models.CharField(max_length = 64)
	user_first_name = models.CharField(max_length = 64)
	direction = models.CharField(max_length = 10)
	target_language = models.CharField(max_length = 2)
	number_of_words = models.IntegerField()

	def __str__(self):
		return f'test_id : {self.id}, user : {self.user_first_name} {self.user} {self.direction}:{self.target_language}'
		
class TestResult(models.Model):

	test = models.ForeignKey(Tests, on_delete = models.CASCADE, related_name = 'test_origin')
	word = models.ForeignKey(NewWords, on_delete = models.CASCADE, related_name = 'tests_included', default = 1)
	tries = models.PositiveSmallIntegerField()
	status = models.BooleanField()

	def __str__(self):
		return f'test_id : {self.test.id}, word : {self.word.word_original}/{self.test.direction} {self.status}:{self.tries}'
