# Generated by Django 3.2.3 on 2021-10-07 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0031_ingredient_useringredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useringredient',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('purchased', 'purchased')], default='new', max_length=300),
        ),
    ]
