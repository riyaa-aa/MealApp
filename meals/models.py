from django.contrib.auth.decorators import login_required
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime, time
from datetime import timedelta

from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.core import validators
from django.db.models.signals import post_save

import re

# Create your models here.

#ingredient model --> name field to store the name of the ingredient
#foreign key back to meal
#each ingredient will relate to one single Meal 
#each person has their own way of interacting with those ingredients
#way of keeping track of user ingredient <= different model
    #foreign key to ingredient(/foreign key to meal) and a foreign key to user
    #at least one other field to track status: choice field
        #two statuses: default status (new) which shows up on the page when no one has interacted with it
        #other status (purchased) 

class Restriction(models.Model):
    description = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return "{}".format(self.description)

class Meal(models.Model):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = "media/")
    ingredients = models.TextField()
    method = models.TextField()
    totalCalories = models.IntegerField(null=True)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    favorited = models.ManyToManyField(User, related_name="faveUser", default=None, blank=True)
    saved = models.ManyToManyField(User, related_name="saveUser", default=None, blank=True)
    restrictions = models.ManyToManyField(Restriction, related_name="meal_restrictions", blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_slogan(meal_time):
        slogan = "Your Meal:"
        if meal_time:
            slogan = f"Your {meal_time.capitalize()}:"
        return slogan
    
    def no_zero_ing(self):
        listIng = self.ingredients.split("\n")
        arr = []
        for i in range(len(listIng)):
            numStr = str(i+1)
            listStr = str(listIng[i])
            this = numStr + ".  " + listStr
            arr.append(this)
        strArr = "\n".join(arr)
        return strArr
    
    def no_zero_met(self):
        listMet = self.method.split("\n")
        arr = []
        for i in range(len(listMet)):
            numStr = str(i+1)
            listStr = str(listMet[i])
            this = numStr + ". " + listStr
            arr.append(this)
        strArr = "\n".join(arr)
        return strArr

    def get_ingredient_list(self):
        list_ing = self.ingredients.split("\n")
        return list_ing

    def generate_user_ingredients(self, user):
        for ingredient in self.ingredientMeal.all():
            UserIngredient.objects.get_or_create(user=user, ingredient=ingredient)

class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="ingredientMeal")

    def __str__(self):
        return "{} ({})".format(self.name, self.meal)

    def split_name(self):
        pattern = r"(([0-9/ ]+ )?(cups?|teaspoons?|tablespoons?|pounds?|ounces?|small|large|cloves?|medium|grams?|litres? )?)"
        matches = re.match(pattern, self.name)
        quantity = matches.group(0)
        ingredient = self.name[matches.end():] # going to the end index of the span to the end of the string, which should just be the ingredient

        return (quantity,ingredient)

class UserIngredient(models.Model):
    STATUS_NEW = "new"
    STATUS_PURCHASED = "purchased"
    STATUSES = [
        (STATUS_NEW,'new'),
        (STATUS_PURCHASED,'purchased')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ingredient_list_user")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="usersIngredient")
    status = models.CharField(max_length=30, choices=STATUSES, default='new')

class Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weight", null=True)
    weight = models.FloatField(validators=[validators.MinValueValidator(20), validators.MaxValueValidator(600)])
    date = models.DateField(default=datetime.date.today)

    class Meta:
        unique_together = [
            ['user','date']
        ]

    def __str__(self):
        return "{} {} {}".format(self.user, self.weight, self.date)

class UserInfo(models.Model):
    RESTRICTIONS = [
        ('vegan', 'vegan'),
        ('vegetarian', 'vegetarian'),
        ('pescatarian', 'pescatarian'),
        ('glutenfree', 'glutenfree'),
        ('lactose', 'lactose'),
        ('nuts', 'nuts'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uInfo")
    lastMeal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="lastMealViewed", blank=True, null=True)
    restrictions = models.ManyToManyField(Restriction, related_name="user_restrictions", blank=True)

    def __str__(self):
        return "{} {}".format(self.user, list(self.restrictions.all().values_list('description',flat=True)))


def check_admin(user):
    return user.is_superuser

def save_user_info(sender, instance, **kwargs):
    UserInfo.objects.get_or_create(user=instance)

post_save.connect(save_user_info, sender=settings.AUTH_USER_MODEL)

