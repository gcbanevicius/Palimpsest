from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from textview import views

urlpatterns = patterns('',
    url(r'^(?P<text_name>[-\w]+)/$', views.index, name='index'),
    url(r'^two_text/(?P<text_name>[-\w]+)/$', views.two_text, name='two_text'),
    url(r'^(?P<text_name>[-\w]+)/two_text$', views.two_text, name='two_text'),
    url(r'(?P<text_name>[-\w]+)/add_comment$', views.add_comment, name='add_comment'),
    url(r'^view_comments/(?P<text_name>[-\w]+)/$', views.view_comments, name='view_comments'),
    url(r'^vocab/(?P<text_name>[-\w]+)/$', views.vocab, name='vocab'),
    #url(r'^two_text', views.two_text, name='two_text')
)

urlpatterns += staticfiles_urlpatterns()
