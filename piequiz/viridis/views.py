from viridis.models import Test
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def index(request):
    tests = Test.objects.order_by('-pub_date')
    return render(request, 'viridis/index.html', { 'tests': tests })

def test(request, test_id, slug):
    test = get_object_or_404(Test, pk=test_id)
    return render(request, 'viridis/test.html', {'test': test})
