# Generated by Django 4.1.4 on 2023-01-06 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]
