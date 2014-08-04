from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'piequiz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^avatar/', include('avatar.urls')),
    (r'^reset/', include('password_reset.urls')),
    url(r'', include('django.contrib.auth.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('viridis.urls', namespace="viridis"))
)
