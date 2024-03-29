# Generated by Django 3.2.3 on 2021-10-01 14:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meals', '0026_alter_weight_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uInfo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='weight',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 1, 22, 30, 51, 948439)),
        ),
    ]
