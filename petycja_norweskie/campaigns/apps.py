from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CampaignsConfig(AppConfig):
    name = 'petycja_norweskie.campaigns'
    verbose_name = _("Campaign")
