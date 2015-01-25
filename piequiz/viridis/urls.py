from django.conf.urls import patterns, url, include
from django.contrib.auth.forms import SetPasswordForm
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from viridis.views import VoteFormView, PopularTestListView, RecentTestListView
from viridis.models import Test
from viridis import views

urlpatterns = patterns('',
    url(r'^$', PopularTestListView.as_view( model=Test, paginate_by=10 ), name='home'),
    url(r'^recently-added/$', RecentTestListView.as_view( model=Test, paginate_by=10 ), name='recent'),
    url(r'^(?P<test_id>\d+)/(?P<slug>[\w-]+)/results/$', views.results, name='results'),
    url(r'^(?P<test_id>\d+)/answer/$', views.answer, name='answer'),
    url(r'^quiz/new$', views.add_test, name='add_test'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/tests/$', views.my_tests, name='my_tests'),
    (r'^search/', include('haystack.urls')),
    (r'^search/autocomplete/', include('haystack.urls')),
    url(r'^vote/$', VoteFormView.as_view(), name="vote"),
    url(r'^(?P<test_id>\d+)/$', RedirectView.as_view(url='slug/')),
    url(r'^questions/add$', views.add_question, name='add_question'),
    url(r'^accounts/password_change/$',
        'django.contrib.auth.views.password_change',
        {'password_change_form': SetPasswordForm},
        name="password_change"),
    url(r'^choices/add$', views.add_choice, name='add_choice'),
    url(r'^(?P<test_id>\d+)/(?P<slug>[\w-]+)/$', views.test, name='test'),
    url(r'^history/$', views.history, name='history'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
