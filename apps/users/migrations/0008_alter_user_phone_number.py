# Generated by Django 4.2 on 2023-11-02 07:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.BigIntegerField(blank=True, error_messages={'unique': 'A user with this phone number already exists.'}, null=True, validators=[django.core.validators.RegexValidator('^989[0-3,9]\\d{8}$', 'Enter a valid mobile number.', 'invalid')], verbose_name='phone number'),
        ),
    ]
