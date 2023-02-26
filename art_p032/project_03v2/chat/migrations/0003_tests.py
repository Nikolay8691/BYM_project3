# Generated by Django 4.1.6 on 2023-02-25 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_newwords'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('user_first_name', models.CharField(max_length=64)),
                ('direction', models.CharField(max_length=10)),
                ('target_language', models.CharField(max_length=2)),
                ('number_of_words', models.IntegerField()),
            ],
        ),
    ]
