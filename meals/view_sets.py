from rest_framework import viewsets
import meals.serializers as meal_serializers
from .models import UserIngredient

# ViewSets define the view behavior.
class UserIngredientViewSet(viewsets.ModelViewSet):
    queryset = UserIngredient.objects.all()
    serializer_class = meal_serializers.UserIngredientSerializer

    def get_queryset(self):
        queryset = UserIngredient.objects.all()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
