from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
   # url(r'^$', 'Palimpsest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^hello_world/', 'Palimpsest.views.hello_world', name='hello_world'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^textview/', include('textview.urls')),

)
