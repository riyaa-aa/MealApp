from django import forms

class WeightTracker(forms.Form):
    dailyweight = forms.FloatField()

class Restrictions(forms.Form):
    RESTRICTIONS = [
        ('vegan', 'vegan'),
        ('vegetarian', 'vegetarian'),
        ('pescatarian', 'pescatarian'),
        ('gluten allergy', 'gluten allergy'),
        ('lactose intolerant', 'lactose intolerant'),
        ('nut allergy', 'nut allergy'),
    ]
    dietRestr = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=RESTRICTIONS,)