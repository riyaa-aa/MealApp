# Generated by Django 3.2.3 on 2021-09-07 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meals', '0020_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restrictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uRestr', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
