# Generated by Django 4.1.6 on 2023-02-08 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_is_verified_user_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='number',
        ),
    ]
