from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from viridis import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^results/(?P<test_id>\d+)/$', views.results, name='results'),
    url(r'^(?P<test_id>\d+)/answer/$', views.answer, name='answer'),
    url(r'^test/new$', views.add_test, name='add_test'),
    (r'^search/', include('haystack.urls')),
    (r'^search/autocomplete/', include('haystack.urls')),
    url(r'^(?P<test_id>\d+)/$', RedirectView.as_view(url='slug/')),
    url(r'^(?P<test_id>\d+)/(?P<slug>[\w-]+)/$', views.test, name='test')
)
