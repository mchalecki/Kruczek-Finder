from django.conf import settings
from django.conf.urls import include, url
from django.views import static

urlpatterns = [
    url(r'^', include('api.urls')),
]

# serving media when debug = True
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns.append(url(
        r'^media/(?P<path>.*)$',
        static.serve, kwargs={
            'document_root': settings.MEDIA_ROOT
        }
    ))
