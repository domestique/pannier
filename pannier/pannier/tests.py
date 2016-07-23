from django.test import TestCase

from pannier import models


class TestLeadModel(TestCase):

    def _create_lead(self, lead_details=None):
        lead_details = lead_details if lead_details else {}
        return models.Lead.create_lead(
            first_name=lead_details.get('first_name', 'Klea'),
            last_name=lead_details.get('last_name', 'Ridley'),
            company_name=lead_details.get('company_name', 'Domestique Studios'),
            domain_name=lead_details.get('domain_name', 'domestique'),
            email_address=lead_details.get('email_address', 'support@domestiquestudios.com'),
            phone_number=lead_details.get('phone_number', '123-123-1234'),
            team_size=lead_details.get('team_size', '1-10'),
        )

    def test_full_name(self):
        lead = self._create_lead()
        self.assertEqual(lead.full_name, 'Klea Ridley')

    def test__str(self):
        lead = self._create_lead()
        self.assertEqual(lead.__str__(), 'Lead: {}'.format(lead.full_name))
