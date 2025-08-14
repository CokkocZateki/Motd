from django import forms
from .models import MotdMessage


class MotdMessageForm(forms.ModelForm):
    class Meta:
        model = MotdMessage
        fields = [
            "title",
            "content",
            "style",
            "start_date",
            "end_date",
            "is_active",
            "show_to_all",
            "restricted_to_groups",
        ]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5, "class": "form-control"}),
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "restricted_to_groups": forms.SelectMultiple(attrs={"class": "form-control select2", "size": "10"}),
            "style": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "style": "Priority Level",
            "show_to_all": "Show to all Members",
        }
        help_texts = {
            "show_to_all": "Show to all users with Member state",
            "restricted_to_groups": "Select specific groups (use Ctrl/Cmd to select multiple)",
        }
