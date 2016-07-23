from django.conf.urls import include, url
from django.contrib import admin

from pannier import urls as pannier_urls

urlpatterns = [
    url(r'^pannier_admin/', admin.site.urls),
    url(r'', include(pannier_urls)),
]
