# Generated by Django 3.2.3 on 2021-08-27 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0013_fave'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='favorited',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Fave',
        ),
    ]
