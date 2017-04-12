from django.contrib import admin

# Register your models here.
from petycja_norweskie.campaigns.models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'organizer', 'site_title', 'site_subtitle')
