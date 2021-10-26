# Generated by Django 3.2.3 on 2021-08-27 13:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meals', '0015_auto_20210827_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='favorited',
            field=models.ManyToManyField(related_name='faveUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
