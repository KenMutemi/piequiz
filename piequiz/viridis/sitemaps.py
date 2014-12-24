from viridis.models import Test

class TestSitemap(Sitemap):
    changefreq = 'never'
    priority = 1

    def items(self):
        return Test.objects.all()

    def lastmod(self, obj):
        return obj.pub_date
