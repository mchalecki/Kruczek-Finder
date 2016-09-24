from django.conf.urls import url

from .views import MainView


urlpatterns = [
    url(r'^$', MainView.as_view(), name='home'),
]