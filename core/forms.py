from django import forms
from .models import Habit, Record

class HabitForm(forms.Form):
    CHOICES = [ ("more", "at least"), ("less", "less than") ]

    verb = forms.CharField(max_length=20,  widget= forms.TextInput
                           (attrs={'placeholder':'verb'}))
    noun = forms.CharField(max_length=20, widget= forms.TextInput
                           (attrs={'placeholder':'plural noun'}))
    noun_singular = forms.CharField(max_length=20, widget= forms.TextInput
                           (attrs={'placeholder':'noun'}))
    number = forms.FloatField(widget= forms.TextInput
                           (attrs={'placeholder':'number'}))
    more_less = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            "number"
        ]
