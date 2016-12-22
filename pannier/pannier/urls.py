from django.conf.urls import url

from pannier.views import docker_hub_view, lead_creation_view, thanks_view


urlpatterns = [
    url(r'^trials/$', lead_creation_view, name='lead-create'),
    url(r'^trials/thanks/$', thanks_view, name='thanks'),
    url(r'^docker/$', docker_hub_view, name='docker'),
]
