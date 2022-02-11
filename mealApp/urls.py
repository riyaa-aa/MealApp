"""mealApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as v
from meals import views as m
#from meals.views import home_view, weight_view, ingredients_view, favorites_view, settings_view
from meals.views import *

urlpatterns = [
    path('', v.signup, name='login'),
    path('admin/', admin.site.urls),
    path("signup/", v.signup, name = 'signup'),
    path('', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('meals.urls')),
    path('logout/', v.signup, name='logout')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)


