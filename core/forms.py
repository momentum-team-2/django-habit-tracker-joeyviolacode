from django import forms
from .models import Habit

class BookForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = [
            "verb",
            "noun",
            "noun_singular",
            "number",
            "is_negative"
        ]