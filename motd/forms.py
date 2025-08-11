from django import forms

from .models import MotdMessage


class MotdMessageForm(forms.ModelForm):
    class Meta:
        model = MotdMessage
        fields = [
            "title",
            "content",
            "priority",
            "style",
            "start_date",
            "end_date",
            "is_active",
            "show_to_all",
            "restricted_to_groups",
        ]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "restricted_to_groups": forms.CheckboxSelectMultiple,
        }

