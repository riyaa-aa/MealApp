from django.urls import path, include
from meals import views, view_sets
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'user_ingredients', view_sets.UserIngredientViewSet)

# Wire up the API using automatic URL routing.
# Include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('redirect_to_specific_meal/', views.redirect_to_specific_meal,
        name='redirect_to_specific_meal'),
    path('home/', views.home_view, name='home'),
    path('weight/', views.weight_view, name='weight'),
    path('ingredients/<int:id>', views.ingredients_add, name='ingredients_add'),
    path('ingredients/', views.ingredients_view, name='ingredients'),
    path('favorites/<int:id>', views.favorites_add, name='favorite_add'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('browse/', views.browseMeals_view, name='browse'),
    path('browse/<str:pk>/', views.meal_list_view, name='mealObject'),
    path('settings/', views.settings_view, name='settings'),
]

