from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^currencies', views.currencies),
    url(r'^currency/(?P<name>\w{3})/$', views.currency),
    url(r'^sequence', views.sequence),
]
