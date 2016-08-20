import os

from mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse

from pannier import forms, models

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, 'test_data')


class BaseCase(TestCase):

    def assertStatusCode(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code)


class TestLeadModel(BaseCase):

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


class TestPannierViews(BaseCase):

    def test_lead_create_get(self):
        response = self.client.get(reverse('lead-create'))
        self.assertStatusCode(response, 200)
        self.assertTrue(
            isinstance(response.context['form'], forms.LeadForm),
        )
        self.assertTemplateUsed('base.html')
        self.assertTemplateUsed('lead.html')

    def test_lead_create(self):
        response = self.client.post(reverse('lead-create'), {
            'first_name': 'Pat',
            'last_name': 'Patterson',
            'company_name': 'Patty Cakes',
            'domain_name': 'itspat',
            'email_address': 'pat@pattycakes.com',
            'phone_number': '321-321-4321',
            'team_size': '10-30',
        })
        self.assertStatusCode(response, 302)
        self.assertRedirects(response, reverse('thanks'))
        lead = models.Lead.objects.get(first_name='Pat')
        self.assertEqual(lead.last_name, 'Patterson')
        self.assertEqual(lead.company_name, 'Patty Cakes')
        self.assertEqual(lead.domain_name, 'itspat')
        self.assertEqual(lead.email_address, 'pat@pattycakes.com')
        self.assertEqual(lead.phone_number, '321-321-4321')
        self.assertEqual(lead.team_size, '10-30')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'New Invite Signup!')

    def test_lead_create_error(self):
        response = self.client.post(reverse('lead-create'), {
            'first_name': 'Pat',
            'last_name': 'Patterson',
            'company_name': 'Patty Cakes',
            'domain_name': 'itspat',
            'email_address': 'pat@pattycakes.com',
            'phone_number': '321-321-4321',
            'team_size': 'BAD TEAM SIZE',
        })
        self.assertStatusCode(response, 200)
        self.assertTemplateUsed('base.html')
        self.assertTemplateUsed('lead.html')
        form = response.context['form']
        self.assertEqual(
            form.errors['team_size'],
            ['Select a valid choice. BAD TEAM SIZE is not one of the available choices.']
        )

    def test_thanks_get(self):
        response = self.client.get(reverse('thanks'))
        self.assertStatusCode(response, 200)
        self.assertTemplateUsed('base.html')
        self.assertTemplateUsed('thanks.html')

    @override_settings(PANNIER_WORKSPACE='/home/workspace/')
    @patch('pannier.views.call')
    def test_docker_webhook(self, call_mock):
        json_data = open(os.path.join(TEST_DIR, 'docker_hook.json')).read()
        response = self.client.post(reverse('docker'), content_type='application/json', data=json_data)
        self.assertStatusCode(response, 200)
        call_mock.assert_called_with(
            './tag_new_version.sh', shell=True, cwd='/home/workspace/'
        )
        self.assertEqual(len(mail.outbox), 1)
