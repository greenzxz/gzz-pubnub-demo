from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_user, name='login'),
    #url(r'^join$', views.join, name='join'),
    #url(r'^channels$', views.channels, name='channels'),
    url(r'^create$', views.create, name='create'),
    url(r'^send_msg$', views.send, name='send'),
    url(r'^sent$', views.sent, name='sent'),
]
