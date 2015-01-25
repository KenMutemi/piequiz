import datetime
import simplejson as json
from django_tables2   import RequestConfig
from viridis.tables import TestTable
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from viridis.forms import AddTestForm, AddQuestionForm, AddChoiceForm, VoteForm
from django.contrib.auth.decorators import login_required, user_passes_test
from haystack.query import SearchQuerySet
from viridis.models import Test, Question, Choice, Vote, History
from itertools import repeat
from django.core import serializers
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict),
content_type='application/json')
        response.status = 200 if valid_form else 500
        return response

class VoteFormBaseView(FormView):
    form_class = VoteForm

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        test = get_object_or_404(Test, pk=form.data["test"])
        user = self.request.user
        prev_votes = Vote.objects.filter(voter=user, test=test)
        has_voted = (len(prev_votes)>0)

        ret = {"success": 1}
        if not has_voted:
            # add vote
            v = Vote.objects.create(voter=user, test=test)
            ret["voteobj"] = v.id
        else:
            # delete vote
            prev_votes[0].delete()
            ret["unvoted"] = 1
        return self.create_response(ret, True)

    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors}

class VoteFormView(JSONFormMixin, VoteFormBaseView):
    pass

@login_required
def profile(request):
    return render(request, 'viridis/profile.html', {"test": test})

@user_passes_test(lambda u: u.is_staff, login_url='/')
@login_required
def my_tests(request):
    test = TestTable(Test.objects.filter(user=request.user.id))
    test.paginate(page=request.GET.get('page', 1), per_page=10)
    # delte selected quizes
    request.POST.get('delete')
    Test.objects.filter(id__in=request.POST.getlist('selection')).delete()
    return render(request, 'viridis/mytests.html', {"test": test})

class PopularTestListView(ListView):
    model = Test
    queryset = Test.with_votes.all()
    popular = 'active'
    def get_context_data(self, **kwargs):
        context = super(PopularTestListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted = Vote.objects.filter(voter=self.request.user)
            tests_in_page = [test.id for test in context["object_list"]]
            voted = voted.filter(test_id__in=tests_in_page)
            voted = voted.values_list('test_id', flat=True)
            context['voted'] = voted
        # Change tab class to active in this page. Not very elegant.
        # TODO: Create a more elegant solution.
        context['popular'] = self.popular
        return context

class RecentTestListView(ListView):
    queryset = Test.objects.order_by('-pub_date')
    recent = 'active'
    def get_context_data(self, **kwargs):
        context = super(RecentTestListView, self).get_context_data(**kwargs)
        # Change tab class to active in this page. Not very elegant.
        # TODO: Create a more elegant solution.
        context['recent'] = self.recent
        return context


def test(request, test_id, slug):
    test = get_object_or_404(Test, pk=test_id)
    if not slug == test.slug:
        return HttpResponsePermanentRedirect(test.get_absolute_url())
    return render(request, 'viridis/test.html', {'test': test})

def answer(request, test_id):
    test = Test.objects.get(pk=test_id)
    request.session['choice_id'] = request.POST.getlist('choice')
    request.session['question_id'] = request.POST.getlist('question_id')

    if request.is_ajax(): # I don't know why but it works
        return render(request, 'viridis/test.html', {'test': test})
    else:
        return HttpResponse("Sorry, please enable javascript in your browser to take this test")


def results(request, test_id, slug):
    test = get_object_or_404(Test, pk=test_id)
    correct_answers = Choice.objects.filter(test_id=test_id, is_correct=True).values_list("id", flat=True)
    y = [unicode(i) for i in correct_answers] # Convert int elements to unicode
    answer_match = set(y).intersection(request.session['choice_id']) # create set
    l_answer_match = list(answer_match) # Convert answer_match to list
    score = len(l_answer_match) * test.marks_per_question # get the total marks of scored by user
    slug = test.slug

    if request.user.is_authenticated():
        try:
            history = History.objects.get(user=request.user, test_id=test.pk)
            history.score = score
            history.save()
        except (ValueError, History.DoesNotExist):
            History.objects.create(user=request.user, test=test.title, test_id=test.pk, score=score, marks=test.marks)
    else:
        pass

    return render(request, 'viridis/results.html',{
        'answer': request.session['choice_id'],
        'score': score,
        'percentage_score': int(float(score)/test.marks*100),
        'test': test })

@login_required(login_url = "/accounts/login/")
def history(request):
    return render(request, 'viridis/history.html', {
        'history': History.objects.filter(user=request.user)
        })

@user_passes_test(lambda u: u.is_staff, login_url='/')
@login_required(login_url = "/accounts/login/")
def add_test(request):
    if request.method == "POST":
        form = AddTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            cd = form.cleaned_data
            test.user_id = request.user.id
            request.session['no_of_question'] = cd['questions']
            request.session['total_marks'] = cd['marks']
            test.marks_per_question = request.session['total_marks']/request.session['no_of_question']
            test.save()
            request.session['test_title'] = test.title
            request.session['test_id'] = test.pk
            return HttpResponseRedirect('/questions/add')
    else:
        form = AddTestForm(label_suffix='')
    return render(request, 'viridis/new_test.html', {
        "form": form
    })

@user_passes_test(lambda u: u.is_staff, login_url='/')
@login_required
def add_question(request):
    """User accesses the add_question view.
    If the number of extra forms has been defined by the user, display them.
    Else, display one form.
    """
    try:
        extra_questions = request.session['no_of_question']
        mark_per_question = (request.session['total_marks']/request.session['no_of_question'])
        request.session['mark_per_question'] = mark_per_question
    except KeyError:
        extra_questions = 1
    QuestionFormSet = formset_factory(AddQuestionForm, extra=extra_questions)
    if request.method == "POST":
        formset = QuestionFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for i in range(0, extra_questions):
                question = Question(
                question_text = request.POST.get('form-' + str(i) + '-question_text'),
                question_pic = request.FILES.get('form-' + str(i) + '-image_file'),
                test_id = request.session['test_id'],
                marks = mark_per_question,
                pub_date = datetime.datetime.now(),
                )
                question.save()
            return HttpResponseRedirect('/choices/add')
    else:
        try:
            formset = QuestionFormSet()
        except KeyError:
            formset = QuestionFormSet()
    return render(request, 'viridis/create_questions.html', {
        "formset": formset,
        "title": request.session['test_title']
    })

@user_passes_test(lambda u: u.is_staff, login_url='/')
@login_required
def add_choice(request):
    """User accesses the add_choice view.
    If the number of extra forms has been defined by the user, display them.
    Else, display one form.
    """
    mark = request.session['mark_per_question']
    test = Test.objects.get(id = request.session['test_id'])
    questions = Question.objects.filter(test_id=test.pk)
    questions_pks = [x.pk for item in questions for x in repeat(item, 4)] # multiply ...
        # pk elements in this list by 4
    try:
        extra_questions = request.session['no_of_question']
    except KeyError:
        extra_questions = 1
    ChoiceFormSet = modelformset_factory(Choice, form=AddChoiceForm, extra=extra_questions*4)
    if request.method == "POST":
        formset = ChoiceFormSet(request.POST)
        if formset.is_valid():
            for i in range(0, extra_questions*4):
                choice = Choice(
                test_id = request.session['test_id'],
                question_id = questions_pks[i],
                choice_text = request.POST.get('form-' + str(i) + '-choice_text'),
                is_correct = request.POST.get('form-' + str(i) + '-mark'),
                )
                choice.save()
            return HttpResponseRedirect('/{0}/'.format(request.session['test_id']))
    else:
        try:
            formset = ChoiceFormSet(queryset=Choice.objects.none())
        except KeyError:
            formset = ChoiceFormSet(queryset=Choice.objects.none())
    return render(request, 'viridis/add_choices.html', {
        "formset": formset,
        "test": test,
        "mark": mark
    })

def autocomplete(request):
    """User enters search term in search box. The system tries
    to match with words similar to what is being input.
    """
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]

    the_data = json.dumps({
        'results' : suggestions # Return json to avoid XSS attack
    })
    return HttpResponse(the_data, content_type='application/json')
