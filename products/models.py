from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"))
    price = models.PositiveIntegerField(_("price"), default=0)
    active = models.BooleanField(_("active"), default=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    