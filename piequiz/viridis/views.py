from django.shortcuts import render
from viridis.models import Test

def index(request):
    tests = Test.objects.order_by('-pub_date')
    return render(request, 'viridis/index.html', { 'tests': tests })
