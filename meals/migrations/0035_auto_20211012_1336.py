# Generated by Django 3.2.3 on 2021-10-12 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meals', '0034_alter_ingredient_meal'),
    ]

    operations = [
        migrations.AddField(
            model_name='useringredient',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_list_user', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useringredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersIngredient', to='meals.ingredient'),
        ),
        migrations.AlterField(
            model_name='useringredient',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('purchased', 'purchased')], default='new', max_length=30),
        ),
    ]