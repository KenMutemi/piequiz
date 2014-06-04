from django.conf.urls import patterns, url, include
from viridis import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^results/(?P<test_id>\d+)/$', views.results, name='results'),
    url(r'^(?P<test_id>\d+)/answer/$', views.answer, name='answer'),
    (r'^search/', include('haystack.urls')),
    (r'^search/autocomplete/', include('haystack.urls')),
    url(r'^(?P<test_id>\d+)/(?P<slug>\w+)/$', views.test, name='test')
)
