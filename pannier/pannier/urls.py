from django.conf.urls import url

from pannier.views import lead_creation_view, thanks_view


urlpatterns = [
    url(r'^trials/$', lead_creation_view, name='lead-create'),
    url(r'^trials/thanks/$', thanks_view, name='thanks'),
]
