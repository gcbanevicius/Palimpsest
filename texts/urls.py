from django.conf.urls import patterns, url

from texts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
