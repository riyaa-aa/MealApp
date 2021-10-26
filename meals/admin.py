from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Meal)
admin.site.register(Weight)
admin.site.register(UserInfo)
admin.site.register(Ingredient)
admin.site.register(UserIngredient)