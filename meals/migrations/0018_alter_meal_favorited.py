# Generated by Django 3.2.3 on 2021-08-30 06:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meals', '0017_meal_saved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='favorited',
            field=models.ManyToManyField(blank=True, default=None, related_name='faveUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
