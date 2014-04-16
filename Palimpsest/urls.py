from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^about/', views.about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('textview.urls')),
    url(r'^textview/', include('textview.urls')),
)
