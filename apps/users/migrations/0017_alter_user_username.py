# Generated by Django 4.2 on 2023-11-07 12:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with this username already exists.'}, help_text='Required. 32 characters or fewer starting with a Lowercase letter. @/./+/-/_ only.', max_length=32, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][a-z0-9_\\.]+$', 'Enter a valid username. This value must contain only Lowercase letter, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username'),
        ),
    ]