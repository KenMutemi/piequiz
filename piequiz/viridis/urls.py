from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from viridis import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^results/(?P<test_id>\d+)/$', views.results, name='results'),
    url(r'^(?P<test_id>\d+)/answer/$', views.answer, name='answer'),
    url(r'^test/new$', views.add_test, name='add_test'),
    url(r'^profile/$', views.profile, name='profile'),
    (r'^search/', include('haystack.urls')),
    (r'^search/autocomplete/', include('haystack.urls')),
    url(r'^(?P<test_id>\d+)/$', RedirectView.as_view(url='slug/')),
    url(r'^question/new$', views.add_question, name='add_question'),
    url(r'^(?P<test_id>\d+)/(?P<slug>[\w-]+)/$', views.test, name='test')
) 

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
