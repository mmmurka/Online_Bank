# Generated by Django 5.0.2 on 2024-02-27 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0002_remove_account_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='identification_number',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
    ]