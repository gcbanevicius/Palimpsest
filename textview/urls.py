from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from textview import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^two_text', views.two_text, name='two_text')
)

urlpatterns += staticfiles_urlpatterns()
