from django.contrib.sitemaps import Sitemap
from viridis.models import Test, Question

class TestSitemap(Sitemap):
    changefreq = 'never'
    priority = 1

    def items(self):
        return Test.objects.all()

    def lastmod(self, obj):
        return obj.pub_date

class QuestionSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1

    def items(self):
        return Question.objects.all()

    def lastmod(self, obj):
        return obj.pub_date
