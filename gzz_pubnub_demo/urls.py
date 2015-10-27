from django.conf.urls import patterns, include, url

from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gzz_pubnub_demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^chat/', include('chatserver.urls', namespace='chatserver')),
    url(r'^$/', views.index),
    url(r'^admin/', include(admin.site.urls)),
)
