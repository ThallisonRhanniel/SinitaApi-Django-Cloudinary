from django.conf.urls import url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib import admin

from Api.views import token_request

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^v1/', include('Api.urls', namespace='api')),
    url(r'^token/', token_request, name='token'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
