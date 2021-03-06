# coding=utf-8
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from petycja_norweskie.campaigns.models import Campaign
from petycja_norweskie.users.models import User

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse


class PetitionQuerySet(models.QuerySet):
    def for_user(self, user: User):
        if user.is_anonymous():
            return self.filter(is_published=True)
        return self

    def for_site(self, site: Site):
        return self.filter(campaign__site=site)

    def for_admin(self, user: User):
        return self.filter(campaign__users=user)


@python_2_unicode_compatible
class Petition(TimeStampedModel):
    campaign = models.ForeignKey(to=Campaign,
                                 verbose_name=_("Campaign"),
                                 on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = models.CharField(verbose_name=_("Slug"),
                            max_length=50,
                            unique=True,
                            help_text=_("Modify to update address of petition"))
    title = models.CharField(verbose_name=_("Title"), max_length=250)
    text = models.TextField(verbose_name=_("Text"))
    overview = models.TextField(verbose_name=_("Overview"),
                                help_text=_("A brief overview of petition subject encouraging "
                                            "the signing of the petition."))
    finish_message = models.TextField(verbose_name=_("Finish message"), help_text=_("Messages shows after signatures"))

    ask_first_name = models.BooleanField(verbose_name=_("Ask first name"), default=False)
    ask_second_name = models.BooleanField(verbose_name=_("Ask second name"), default=False)
    ask_organization = models.BooleanField(verbose_name=_("Ask organization"), default=True)
    ask_city = models.BooleanField(verbose_name=_("Ask about city"), default=True)
    ask_email = models.BooleanField(verbose_name=_("Ask about e-mail"), default=False)

    first_name_label = models.CharField(verbose_name=_("Label for first name field"),
                                        max_length=100,
                                        default=_("First name"))
    second_name_label = models.CharField(verbose_name=_("Label for second name field"),
                                         max_length=100,
                                         default=_("Second name"))
    organization_label = models.CharField(verbose_name=_("Label for organization field"),
                                          max_length=100,
                                          default=_("Organization"))
    city_label = models.CharField(verbose_name=_("Label for city field"),
                                  max_length=100,
                                  default=_("City"))
    email_label = models.CharField(verbose_name=_("Label for email field"),
                                   max_length=100,
                                   default=_("E-mail"))
    sign_button_text = models.CharField(max_length=50, default=_("Sign"), help_text=_("Sign button text"))

    paginate_by = models.SmallIntegerField(default=50,
                                           verbose_name=_("Paginate signatures by"),
                                           help_text=_("Specifies the number of signatures per signatures page"))
    is_published = models.BooleanField(default=False, verbose_name=_("Is published on site?"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is open to new signatures?"))
    front = models.BooleanField(default=True,
                                verbose_name=_("Is available on front-view?"),
                                help_text=_("There should be only one available sites"))
    disabled_warning = models.TextField(verbose_name=_("Message of disabled signature warning"),
                                        default=_("The ability to sign under this petition has been disabled."),
                                        help_text=_("A message when someone is trying to inject a signature, "
                                                    "despite turning off the form."))
    disabled_message = models.TextField(verbose_name=_("Text of disabled signature message"),
                                        default=_("The ability to sign under this petition has been disabled."),
                                        help_text=_("A message posted on the page if the signature is disabled."))
    objects = PetitionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Petition")
        verbose_name_plural = _("Petitions")
        ordering = ['created', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('petitions:petition', kwargs={'slug': self.slug})


class PermissionDefinition(models.Model):
    petition = models.ForeignKey(Petition, help_text=_("Petition"), on_delete=models.CASCADE)
    text = models.TextField()
    default = models.BooleanField(verbose_name=_("Default checked"),
                                  default=True,
                                  help_text=_("Define default check on permission field"))
    required = models.BooleanField(verbose_name=_("Check required"),
                                   default=True,
                                   help_text=_("Define the field is required or not"))
    ordering = models.PositiveSmallIntegerField(default=1, help_text=_("Define orders of the permissions in form"))

    class Meta:
        verbose_name = _("Definition")
        verbose_name_plural = _("Definitions")


class SignatureQuerySet(models.QuerySet):
    def for_admin(self, user: User):
        return self.filter(petition__campaign__users=user)


@python_2_unicode_compatible
class Signature(TimeStampedModel):
    petition = models.ForeignKey(Petition, verbose_name=_("Petition"), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, verbose_name=_("First name"))
    second_name = models.CharField(max_length=50, blank=True, verbose_name=_("Second name"))
    organization = models.CharField(max_length=100, blank=True, verbose_name=_("Organization"))
    city = models.CharField(max_length=50, blank=True, verbose_name=_("City"))
    email = models.EmailField(verbose_name=_("E-mail"), blank=True)
    counter = models.SmallIntegerField(verbose_name=_("No."))
    objects = SignatureQuerySet.as_manager()

    class Meta:
        verbose_name = _("Signature")
        verbose_name_plural = _("Signatures")
        ordering = ['created', ]

    def __str__(self):
        if self.first_name or self.second_name:
            return "{} {}".format(self.first_name, self.second_name)
        return self.organization


class Permission(models.Model):
    definition = models.ForeignKey(PermissionDefinition, verbose_name=_("Definition"), on_delete=models.CASCADE)
    signature = models.ForeignKey(Signature, verbose_name=_("Signature"), on_delete=models.CASCADE)
    value = models.BooleanField(verbose_name=_("Value"))

    class Meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")


def update_counter(sender, instance, **kwargs):
    if instance.counter is None and instance.petition is not None:
        instance.counter = (Signature.objects.filter(petition=instance.petition).count() + 1)
