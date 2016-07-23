from django.db import models


class BaseModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created']
        app_label = 'pannier'


class Lead(BaseModel):

    TEAM_SIZE = (
        ('1-10', '1-10'),
        ('10-30', '10-30'),
        ('30-50', '30-50'),
        ('50+', '50+')
    )

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    company_name = models.CharField(max_length=128, blank=True)
    domain_name = models.CharField(
        max_length=128,
        help_text='Domain name you wish to have, e.g: company.demoti.me',
    )
    email_address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16, blank=True)
    team_size = models.CharField(max_length=24, choices=TEAM_SIZE)
    contacted = models.BooleanField(default=False)

    def __str__(self):
        return 'Lead: {}'.format(self.full_name)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @classmethod
    def create_lead(cls, first_name, last_name, company_name,
                    domain_name, email_address, phone_number, team_size):
        obj = cls.objects.create(
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            domain_name=domain_name,
            email_address=email_address,
            phone_number=phone_number,
            team_size=team_size
        )
        return obj
