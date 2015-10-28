from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.chat, name='chat'),
    url(r'^get_keys$', views.get_user_keys, name='getkeys'),
    url(r'^send_msg$', views.send, name='send'),
    url(r'^sent$', views.sent, name='sent'),
]
