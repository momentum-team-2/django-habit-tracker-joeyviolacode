from django import forms
from .models import Habit, Record

class HabitForm(forms.Form):
    CHOICES = [ ("more", "at least"), ("less", "less than") ]

    verb = forms.CharField(max_length=20,  widget= forms.TextInput
                           (attrs={'placeholder':'verb', 'size':10}))
    noun = forms.CharField(max_length=20, widget= forms.TextInput
                           (attrs={'placeholder':'plural noun', 'size':10}))
    noun_singular = forms.CharField(max_length=20, widget= forms.TextInput
                           (attrs={'placeholder':'noun', 'size':10}))
    number = forms.FloatField(widget= forms.TextInput
                           (attrs={'placeholder':'number', 'size':8}))
    more_less = forms.ChoiceField(choices=CHOICES, widget=forms.Select)


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            "number"
        ]
