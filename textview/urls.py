from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from textview import views

urlpatterns = patterns('',
    url(r'^(?P<text_name>[-\w]+)/$', views.index, name='index'),
    url(r'^two_text/(?P<text_name>[-\w]+)/$', views.two_text, name='two_text'),
    url(r'^(?P<text_name>[-\w]+)/two_text$', views.two_text, name='two_text'),
    url(r'^view_comments/(?P<text_name>[-\w]+)/$', views.view_comments, name='view_comments'),
    url(r'(?P<text_name>[-\w]+)/view_comments$', views.view_comments, name='view_comments'),
    url(r'(?P<text_name>[-\w]+)/add_comment$', views.add_comment, name='add_comment'),
    url(r'add_comment/(?P<text_name>[-\w]+)/$', views.add_comment, name='add_comment'),
    url(r'^vocab/(?P<text_name>[-\w]+)/$', views.vocab, name='vocab'),
    url(r'^view_critical/(?P<text_name>[-\w]+)/(?P<isbn_num>[-\w]+:*[-\d]+[-\w]*)$', views.view_critical, name='view_critical'),
    #url(r'^two_text', views.two_text, name='two_text')
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
)

urlpatterns += staticfiles_urlpatterns()
