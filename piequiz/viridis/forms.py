from django import forms
from viridis.models import Test

class AddTestForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'text'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'text', 'title':'not required'}))
    mark = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control mark-test', 'type':'number'}))
    questions = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'number', 'title':'number of questions'}))

