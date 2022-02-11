from django.contrib import admin

# Register your models here.

from meals import models as m

admin.site.register(m.Meal)
admin.site.register(m.Weight)
admin.site.register(m.UserInfo)
admin.site.register(m.Ingredient)
admin.site.register(m.UserIngredient)
admin.site.register(m.Restriction)