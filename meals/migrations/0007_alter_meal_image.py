# Generated by Django 3.2.3 on 2021-08-17 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0006_alter_weight_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='image',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
