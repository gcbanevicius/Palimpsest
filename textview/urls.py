from django.conf.urls import patterns, url

from textview import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
