from django.views.generic import TemplateView
from django.shortcuts import redirect

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
            return redirect('thanks')

        return self.get(request, *args, **kwargs)


class ThankYouView(TemplateView):

    template_name = 'pannier/thanks.html'


lead_creation_view = LeadCreationView.as_view()
thanks_view = ThankYouView.as_view()
