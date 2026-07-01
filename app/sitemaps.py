from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)