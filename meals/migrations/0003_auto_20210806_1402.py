# Generated by Django 3.2.3 on 2021-08-06 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_auto_20210806_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weight',
            name='number',
        ),
        migrations.RemoveField(
            model_name='weight',
            name='placebo',
        ),
    ]
