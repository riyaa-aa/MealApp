# Generated by Django 3.2.3 on 2021-08-27 13:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meals', '0014_auto_20210827_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='favorited',
        ),
        migrations.AddField(
            model_name='meal',
            name='favorited',
            field=models.ManyToManyField(null=True, related_name='faveUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
