from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.success),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.add),
    url(r'^add_trip$', views.add_trip),
    url(r'^travels/destination/(?P<number>\d+)$', views.display),
    url(r'^travels/destination/(?P<number>\d+)/join$', views.join),
]