from django import forms

from meals.models import UserInfo

class WeightTracker(forms.Form):
    dailyweight = forms.FloatField()

class Restrictions(forms.ModelForm):
    # RESTRICTIONS = [
    #     ('vegan', 'vegan'),
    #     ('vegetarian', 'vegetarian'),
    #     ('pescatarian', 'pescatarian'),
    #     ('gluten allergy', 'gluten allergy'),
    #     ('lactose intolerant', 'lactose intolerant'),
    #     ('nut allergy', 'nut allergy'),
    # ]
    # dietRestr = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=RESTRICTIONS,)
    
    class Meta:
        model = UserInfo
        fields = ['restrictions']
        widgets = {
            'restrictions':forms.CheckboxSelectMultiple()
        }
    
    # customising the widget
    # def __init__(self, *args, **kwargs): # overriding a function inhereted from the class
    #     super().__init__(*args, **kwargs)
    #     self.fields['restrictions'].widget = forms.CheckboxSelectMultiple
