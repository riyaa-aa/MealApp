from django import forms

from meals.models import UserInfo

class WeightTracker(forms.Form):
    dailyweight = forms.FloatField()

class Restrictions(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['restrictions']
        widgets = {
            'restrictions':forms.CheckboxSelectMultiple()
        }
