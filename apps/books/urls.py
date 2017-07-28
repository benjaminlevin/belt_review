from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^delete$', views.delete),   
    url(r'^deletea$', views.deletea),
    url(r'^logout$', views.logout),
    url(r'^books$', views.books),
    url(r'^add$', views.add),
    url(r'^addbr$', views.addbr),
    url(r'^users/(?P<id>\d+)$', views.users),   
    url(r'^books/(?P<id>\d+)$', views.book),
    url(r'^addr/(?P<id>\d+)$', views.addr),                             
]