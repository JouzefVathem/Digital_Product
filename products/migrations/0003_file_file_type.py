# Generated by Django 4.2 on 2023-09-19 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_file_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Audio'), (2, 'Video'), (3, 'PDF')], default=2, verbose_name='file type'),
            preserve_default=False,
        ),
    ]
