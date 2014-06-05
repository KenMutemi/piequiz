from django import forms
from viridis.models import Test

class AddTestForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'text'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'text'}))
    mark = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control mark-test', 'type':'number'}))
    no_of_question = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'number'}))

