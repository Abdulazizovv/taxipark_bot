# Generated by Django 5.0.1 on 2025-03-13 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=15)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
    ]
