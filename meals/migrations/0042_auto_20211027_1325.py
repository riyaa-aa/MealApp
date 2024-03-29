# Generated by Django 3.2.3 on 2021-10-27 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0041_auto_20211027_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='restrictions',
            field=models.ManyToManyField(blank=True, related_name='meal_restrictions', to='meals.Restriction'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='restrictions',
            field=models.ManyToManyField(blank=True, related_name='user_restrictions', to='meals.Restriction'),
        ),
    ]
