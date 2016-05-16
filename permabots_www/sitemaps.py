from django.contrib import sitemaps
from django.core.urlresolvers import reverse

class StaticViewSitemap(sitemaps.Sitemap):

    def items(self):
        return ['home', 'swagger:django.swagger.base.view', 'getting-started']

    def location(self, item):
        return reverse(item)
    
sitemaps = {
    'static': StaticViewSitemap,
}