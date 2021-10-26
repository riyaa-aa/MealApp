from django import template
import meals.models as m

register = template.Library()

@register.simple_tag
def meal_is_user_favorite(meal_id, user_id):
    this_meal = m.Meal.objects.get(pk=meal_id)
    return this_meal.favorited.filter(pk=user_id).exists()

@register.simple_tag
def meal_is_user_saved(meal_id, user_id):
    this_meal = m.Meal.objects.get(pk=meal_id)
    return this_meal.saved.filter(pk=user_id).exists()