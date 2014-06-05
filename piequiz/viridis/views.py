import datetime
import simplejson as json
from viridis.forms import AddTestForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet
from viridis.models import Test, Question, Choice, Answer
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

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
            request.session['no_of_question'] = cd['no_of_question']
            test = Test(
                user_id = request.user.id,
                pub_date = datetime.datetime.now(),
                title = cd['title'],
                institution = cd['institution'],
                marks = cd['mark'],
                slug = slugify(cd['title']),
            )
            test.save()
	    
            return HttpResponseRedirect('/test/new')
    else:
        form = AddTestForm(label_suffix='')
    return render(request, 'viridis/new_test.html', {
        "form": form
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
