# Django
from django import forms

from .models import MotdMessage


class MotdMessageForm(forms.ModelForm):
    class Meta:
        model = MotdMessage
        exclude = ["created_by"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5, "class": "form-control"}),
            "start_date": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "end_date": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "restricted_to_states": forms.SelectMultiple(
                attrs={"class": "form-control select2", "size": "10"}
            ),
            "restricted_to_groups": forms.SelectMultiple(
                attrs={"class": "form-control select2", "size": "10"}
            ),
            "style": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }
