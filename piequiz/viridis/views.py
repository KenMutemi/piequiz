import datetime
import simplejson as json
from os.path import join as pjoin  
from django_tables2   import RequestConfig
from viridis.tables import TestTable
from django.forms.formsets import formset_factory
from viridis.forms import AddTestForm, AddQuestionForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet
from viridis.models import Test, Question, Choice, Answer
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

@login_required
def profile(request):
    return render(request, 'viridis/profile.html', {"test": test})

@login_required
def my_tests(request):
    test = TestTable(Test.objects.filter(user=request.user.id))
    test.paginate(page=request.GET.get('page', 1), per_page=10)
    return render(request, 'viridis/mytests.html', {"test": test})

def index(request):
    tests = Test.objects.order_by('-pub_date')
    return render(request, 'viridis/index.html', { 'tests': tests })

def test(request, test_id, slug):
    test = get_object_or_404(Test, pk=test_id)
    if not slug == test.slug:
        return HttpResponsePermanentRedirect(test.get_absolute_url())
    return render(request, 'viridis/test.html', {'test': test})

def answer(request, test_id):
    test = Test.objects.get(pk=test_id)
    try:
        selected_choice = Answer(
            choice_id = request.POST.get('choice'),
            test = test.id,
            user = request.user.id,
            answer_date = datetime.datetime.now()
        )
        selected_choice.save()
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the test form
        return render(request, 'viridis/test.html', {
            'test': test, 'error_message': "You didn't answer the questions",})
    else:
        selected_choice.save()
        return HttpResponseRedirect(reverse('viridis:results', args=(test.id,)))

def results(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    return render(request, 'viridis/results.html', {'test': test})

@login_required(login_url = "/accounts/login/")
def add_test(request):
    if request.method == "POST":
        form = AddTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            request.session['no_of_question'] = cd['questions']
            test = Test(
                user_id = request.user.id,
                pub_date = datetime.datetime.now(),
                title = cd['title'],
                institution = cd['institution'],
                marks = cd['mark'],
                slug = slugify(cd['title']),
            )
            test.save()
	    
            return HttpResponseRedirect('/question/new')
    else:
        form = AddTestForm(label_suffix='')
    return render(request, 'viridis/new_test.html', {
        "form": form
    })

@login_required(login_url = "/accounts/login/")
def add_question(request):
    """User accesses the add_question view.
    If the number of extra forms has been defined by the user, display them.
    Else, display one form.
    """
    try:
        extra_questions = request.session['no_of_question']
    except KeyError:
        extra_questions = 1
    QuestionFormSet = formset_factory(AddQuestionForm, extra=extra_questions)
    if request.method == "POST":
        formset = QuestionFormSet(request.POST)
        if formset.is_valid():
            for i in range(0, extra_questions):
                question = Question(
                question_text = request.POST.get('form-' + str(i) + '-question_text'),
                test_id = request.POST.get('form-' + str(i) + '-test_id'),
                marks = request.POST.get('form-' + str(i) + '-mark'),
                pub_date = datetime.datetime.now(),
                )
                question.save()
            return HttpResponseRedirect('/test/new')
    else:
        try:
            formset = QuestionFormSet()
        except KeyError:
            formset = QuestionFormSet()
    return render(request, 'viridis/create_questions.html', {
        "formset": formset
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

def approve(request):
    vars = {}
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        test = get_object_or_404(Test, slug=slug)

        approved, created = Approve.objects.create(test=test)

        try:
            user_approved = Test.objects.get(test=test, user=user)
        except:
            user_approved = None

        if user_approved:
            user_approved.total_likes -= 1
            approved.user.remove(request.user)
            user_approved.save()
        else:
            approved.user.add(request.user)
            approved.total_likes += 1
            approved.save()


    return HttpResponse(json.dumps(vars),
                    mimetype='application/javascript')
