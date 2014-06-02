from viridis.models import Test
from viridis.forms import ChoiceForm
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404
from django.forms.formsets import formset_factory

def index(request):
    tests = Test.objects.order_by('-pub_date')
    return render(request, 'viridis/index.html', { 'tests': tests })

def test(request, test_id, slug):
    test = get_object_or_404(Test, pk=test_id)
    if not slug == test.slug:
        return HttpResponsePermanentRedirect(test.get_absolute_url())
    ChoiceFormSet = formset_factory(ChoiceForm)
    formset = ChoiceFormSet()
    return render(request, 'viridis/test.html', {'test': test, 'formset': formset})
