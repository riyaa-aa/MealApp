from django import template
import meals.models as m
from django.contrib.auth import get_user_model

register = template.Library()

@register.simple_tag
def meal_is_user_favorite(meal_id, user_id):
    this_meal = m.Meal.objects.get(pk=meal_id)
    return this_meal.favorited.filter(pk=user_id).exists()

@register.simple_tag
def meal_is_user_saved(meal_id, user_id):
    this_meal = m.Meal.objects.get(pk=meal_id)
    return this_meal.saved.filter(pk=user_id).exists()

def user_is_admin(user_id):
    user =  get_user_model().objects.get(pk=user_id)
    return m.check_admin(user)

register.filter("user_is_admin",user_is_admin)