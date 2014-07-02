from django import forms
from django.forms import ModelForm
from viridis.models import Test, Question, Choice, Vote


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseModelForm, self).__init__(*args, **kwargs)

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseForm, self).__init__(*args, **kwargs)

class AddTestForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'text'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'text', 'title':'not required'}))
    marks = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control mark-test', 'type':'number'}))
    questions = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'number', 'title':'number of questions'}))
    class Meta:
        model = Test
        fields = ['title', 'institution', 'marks']

class AddQuestionForm(BaseForm):
    question_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':2, 'cols': 15}), label="Question")
    #image_file = forms.FileField(required=False)
    #mark = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control mark-question', 'type':'number'}))
   
class AddChoiceForm(BaseModelForm):
    #choice_id = forms.ModelChoiceField(queryset = Question.objects.order_by('-pub_date'), empty_label=None, widget=forms.Select(attrs={'class' : 'form-control test-select'}), label="Question")
    choice_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':2, 'cols': 18}), label="Choice")
    mark = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control mark-question', 'type':'number'}))

    class Meta:
        model = Choice
        fields = ['choice_text', 'mark']

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
