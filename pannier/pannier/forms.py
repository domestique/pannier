from django import forms

from pannier import models


class LeadForm(forms.ModelForm):

    class Meta:
        model = models.Lead
        fields = [
            'first_name', 'last_name', 'company_name', 'domain_name',
            'email_address', 'phone_number', 'team_size'
        ]
