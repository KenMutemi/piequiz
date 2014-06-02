from django import forms
from viridis.models import Choice

class ChoiceForm(forms.Form):
    choice = forms.ModelMultipleChoiceField(queryset=Choice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)
