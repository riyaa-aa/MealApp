# Generated by Django 3.2.3 on 2021-10-27 13:25

from django.db import migrations
from django.apps import apps

def populate_meal_restrictions(apps_config, schema_editor):
    
    Meal = apps.get_model('meals','Meal')
    Restriction = apps.get_model('meals','Restriction')
    
    restriction_vegan = Restriction.objects.get(description="vegan")
    restriction_vegetarian = Restriction.objects.get(description="vegetarian")
    restriction_pescatarian = Restriction.objects.get(description="pescatarian")
    restriction_glutenfree = Restriction.objects.get(description="glutenfree")
    restriction_lactose = Restriction.objects.get(description="lactose")
    restriction_nuts = Restriction.objects.get(description="nuts")


    for meal in Meal.objects.all():
        if meal.vegan:
            meal.restrictions.add(restriction_vegan)
        if meal.vegetarian:
            meal.restrictions.add(restriction_vegetarian)
        if meal.pescatarian:
            meal.restrictions.add(restriction_pescatarian)
        if meal.glutenfree:
            meal.restrictions.add(restriction_glutenfree)
        if meal.lactose:
            meal.restrictions.add(restriction_lactose)
        if meal.nuts:
            meal.restrictions.add(restriction_nuts)

class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0042_auto_20211027_1325'),
    ]

    operations = [
        migrations.RunPython(populate_meal_restrictions),
    ]