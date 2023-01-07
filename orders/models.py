from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Order(models.Model):

    """ Store general order information for a user to checkout """

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),

    )
    is_paid = models.BooleanField(_("paid"), default=False)

    first_name = models.CharField(_("name"), max_length=100)
    last_name = models.CharField(_("family_name"), max_length=100)
    phone_number = models.CharField(_("Phone_number"), max_length=15)
    address = models.CharField(_("address"), max_length=700)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
