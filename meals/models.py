from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import random
import datetime, time
from datetime import timedelta

from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.core import validators

import tkinter
from tkinter import *
from tkinter import messagebox

from django.db.models.fields import CharField

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
    weight = models.FloatField(validators=[validators.MinValueValidator(20), validators.MaxValueValidator(500)])
    date = models.DateField(default=datetime.date.today)

    class Meta:
        unique_together = [
            ['user','date']
        ]

    #def __str__(self):
        #return self.weight

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
    lastMeal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="lastMealViewed", null=True)
    restrictions = models.ManyToManyField(Restriction, related_name="user_restrictions", blank=True)

    def __str__(self):
        return "{}{}".format(self.user, self.restrictions)



