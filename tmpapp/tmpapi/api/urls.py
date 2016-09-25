from django.conf.urls import url

from .views import MainView, ResultView


urlpatterns = [
    url(r'^$', MainView.as_view(), name='home'),
    url(r'^(?P<token>[0-9a-f\-]{36})/$', ResultView.as_view(), name='result')
]