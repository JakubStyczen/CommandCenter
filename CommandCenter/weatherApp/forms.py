from django import forms
from .models import WeatherConditions


class WeatherConditionsForm(forms.ModelForm):
    class Meta:
        model = WeatherConditions
        fields = "__all__"
        labels = {
            "condition_id": "Condition ID",
            "time": "Time",
            "temperature": "Temperature",
            "additional_info": "Additional information",
        }
        widgets = {
            "condition_id": forms.NumberInput(
                attrs={"placeholder": "e.g. 1", "class": "form-control"}
            ),
            "time": forms.DateTimeField(),
            "temperature": forms.NumberInput(
                attrs={"placeholder": "25.5", "class": "form-control"}
            ),
            "additional_info": forms.TextInput(
                attrs={"placeholder": "e.g Good weather...", "class": "form-control"}
            ),
        }
