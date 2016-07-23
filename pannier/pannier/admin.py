from django.contrib import admin

from pannier import models


def full_name(obj):
    return obj.full_name
full_name.short_description = "Name"


class LeadAdmin(admin.ModelAdmin):

    date_hierarchy = 'modified'
    list_display = (
        full_name, 'email_address', 'company_name', 'team_size', 'contacted',
    )
    list_editable = ('contacted', )
    list_filter = ('contacted', 'team_size')

admin.site.register(models.Lead, LeadAdmin)
