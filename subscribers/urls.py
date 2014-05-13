from django.conf.urls import patterns, url


from subscribers import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^signin\?next=(?P<page_name>.+)$', views.signin, name='signin'),
    url(r'^validate/$', views.validate, name='validate'),
    url(r'^signout$', views.signout, name='signout'),
    url(r'^login_error$', views.login_error, name='login_error'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^signup_check/$', views.signup_check, name='signup_check'),                     
    url(r'^(?P<user_name>.+)/$', views.profile, name='profile'),

)
