# Generated by Django 5.0.1 on 2025-03-13 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botapp', '0002_remove_botuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botuser',
            name='user_id',
            field=models.BigIntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
