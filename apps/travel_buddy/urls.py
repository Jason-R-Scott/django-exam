from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels/$', views.travels),
    url(r'^join/(?P<id>\d+)/$', views.join),
    url(r'^view/(?P<id>\d+)/$', views.view),
    url(r'^new/$', views.new),
    url(r'^create/$', views.create),
    url(r'^destroy/(?P<id>\d+)/$', views.destroy),
    url(r'^cancel/(?P<id>\d+)/$', views.cancel)
]