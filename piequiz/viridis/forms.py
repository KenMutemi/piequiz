from django import forms
from django.forms import ModelForm
from viridis.models import Test, Question

class AddTestForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'text'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'text', 'title':'not required'}))
    mark = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control mark-test', 'type':'number'}))
    questions = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'number', 'title':'number of questions'}))

class AddQuestionForm(forms.Form):
    test_id = forms.ModelChoiceField(queryset = Test.objects.order_by('-pub_date'), empty_label=None, widget=forms.Select(attrs={'class' : 'form-control test-select'}), label="Test")
    question_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':2, 'cols': 15}), label="Question")
    #image_file = forms.FileField(required=False)
    mark = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control mark-question', 'type':'number'}))

class AddChoiceForm(forms.Form):
    choice_id = forms.ModelChoiceField(queryset = Question.objects.order_by('-pub_date'), empty_label=None, widget=forms.Select(attrs={'class' : 'form-control test-select'}), label="Question")
    choice_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':2, 'cols': 15}), label="Choice")
    mark = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control mark-question', 'type':'number'}))

