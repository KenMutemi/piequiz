from django.conf.urls import patterns, include, url
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import FlatPageSitemap
from viridis.sitemaps import TestSitemap
from django.contrib import admin
admin.autodiscover()

sitemaps = {
    'flatpages': FlatPageSitemap,
    'test': TestSitemap,
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'piequiz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^reset/', include('password_reset.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('django.contrib.auth.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('viridis.urls', namespace="viridis")),
    url(r'^blog/', include('cms.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
)
