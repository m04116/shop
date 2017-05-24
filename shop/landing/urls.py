from django.conf.urls import include, url

from landing import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
]
