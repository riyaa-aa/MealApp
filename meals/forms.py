from django import forms

from meals.models import UserInfo, Weight

class WeightTracker(forms.ModelForm):
    class Meta:
        model = Weight
        fields = ['weight']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['weight'].label = ""

class Restrictions(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['restrictions']
        widgets = {
            'restrictions':forms.CheckboxSelectMultiple()
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['restrictions'].label = ""
