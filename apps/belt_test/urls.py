from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.success),
    url(r'^logout$', views.logout),
    # url(r'^add_book$', views.add_book),
    # url(r'^add$', views.add),
    # url(r'^books/(?P<number>\d+)$', views.display),
    # url(r'^books/(?P<number>\d+)/new_review$', views.add_review),
    # url(r'^users/(?P<number>\d+)$', views.user_display),
    # url(r'^books/(?P<book_number>\d+)/delete/(?P<review_number>\d+)$', views.delete),
]