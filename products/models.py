from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


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
    

class Comment(models.Model):
    PRODUCT_STARS = (
        ("1", _("Very Bad")),
        ("2", _("Bad")),
        ("3", _("Normal")),
        ("4", _("Good")),
        ("5", _("Perfect")),
    )

    author = models.ForeignKey(
        get_user_model(),
        verbose_name=_("author"),
        on_delete=models.CASCADE,
        related_name="comments",
    )

    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="comments",
    )

    text = models.TextField(_("text"),)
    active = models.BooleanField(_("active"), default=True)
    stars = models.CharField(_("stars"), max_length=10, choices=PRODUCT_STARS, blank=True)
    
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.product.title}: {self.text}"
    