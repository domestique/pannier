import json

from subprocess import call

from django.conf import settings
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from pannier import forms, models


class LeadCreationView(TemplateView):

    template_name = 'pannier/lead.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.form = forms.LeadForm(request.POST)
        else:
            self.form = forms.LeadForm()

        return super(LeadCreationView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LeadCreationView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            data = self.form.cleaned_data
            models.Lead.create_lead(**data)
            send_mail(
                subject='New Invite Signup!',
                message='Someone new has filled out the Invite form!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['support@domestiquestudios.com'],
                fail_silently=True
            )
            return redirect('thanks')

        return self.get(request, *args, **kwargs)


class ThankYouView(TemplateView):

    template_name = 'pannier/thanks.html'


class DockerHubView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DockerHubView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if settings.PANNIER_WORKSPACE or settings.DT_WORKSPACE:
            data = json.loads(request.body.decode('utf-8'))
            if data['push_data']['tag'] == 'latest':
                command = './tag_new_version.sh'
                repo_name = data['repository']['name']

                if repo_name == 'pannier':
                    work_dir = settings.PANNIER_WORKSPACE
                else:
                    work_dir = settings.DT_WORKSPACE

                call(command, shell=True, cwd=work_dir)
                send_mail(
                    subject='New {} Version Pushed'.format(repo_name),
                    message='A new version of {} has been tagged'.format(repo_name),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['support@domestiquestudios.com'],
                    fail_silently=True
                )
        return HttpResponse(status=200)

lead_creation_view = LeadCreationView.as_view()
thanks_view = ThankYouView.as_view()
docker_hub_view = DockerHubView.as_view()
