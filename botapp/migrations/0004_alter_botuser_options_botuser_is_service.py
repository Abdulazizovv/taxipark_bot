# Generated by Django 5.0.1 on 2025-03-14 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botapp', '0003_alter_botuser_user_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='botuser',
            options={'ordering': ['-created_at'], 'verbose_name': 'Bot foydalanuvchisi', 'verbose_name_plural': 'Bot foydalanuvchilari'},
        ),
        migrations.AddField(
            model_name='botuser',
            name='is_service',
            field=models.BooleanField(default=False),
        ),
    ]
