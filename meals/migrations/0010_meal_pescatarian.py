# Generated by Django 3.2.3 on 2021-08-23 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0009_auto_20210820_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='pescatarian',
            field=models.BooleanField(default=False),
        ),
    ]
