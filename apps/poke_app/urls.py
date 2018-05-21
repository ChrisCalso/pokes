from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dash$', views.dash),
    url(r'^createPoke/(?P<user_id>\d+)$', views.createPoke),
    url(r'^logout$', views.logout)
]
