from rest_framework import serializers
from .models import UserIngredient

# Serializers define the API representation.
class UserIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIngredient
        fields = ['pk', 'status']
