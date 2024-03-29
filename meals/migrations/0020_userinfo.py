# Generated by Django 3.2.3 on 2021-09-07 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meals', '0019_alter_meal_saved'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vegan', models.BooleanField(default=False)),
                ('vegetarian', models.BooleanField(default=False)),
                ('pescatarian', models.BooleanField(default=False)),
                ('lactoseIntolerant', models.BooleanField(default=False)),
                ('glutenAllergy', models.BooleanField(default=False)),
                ('nutAllergy', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uInfo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
