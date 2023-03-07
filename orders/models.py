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
    zarinpal_authority = models.CharField(max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(max_length=150, blank=True)
    zarinpal_data = models.TextField(blank=True)

    first_name = models.CharField(_("name"), max_length=100)
    last_name = models.CharField(_("family_name"), max_length=100)
    phone_number = models.CharField(_("Phone_number"), max_length=15)
    address = models.CharField(_("address"), max_length=700)

    order_notes = models.TextField(_("order_notes"), blank=True)

    datetime_created = models.DateTimeField(_("order_datetime"), auto_now_add=True)
    datetime_modified = models.DateTimeField(_("checkout_datetime"), auto_now=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")


    def __str__(self):

        return f"Order {self.id}"


    def get_total_price(self):

        return sum(item.quantity * item.price for item in self.items.all())


class OrderItem(models.Model):
    
    """ Include cart products data to pay """

    order = models.ForeignKey(

        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("order"),

    )

    product = models.ForeignKey(

        "products.Product",
        on_delete=models.CASCADE,
        verbose_name=_("product"),

    )

    quantity = models.PositiveIntegerField(_("quantity"), default=1)
    price = models.PositiveIntegerField(_("price"))

    class Meta:
        verbose_name = _("orderitem")
        verbose_name_plural = _("orderitems")

    def __str__(self):
        return f"OrderItem {self.id}: {self.product} * {self.quantity} (price:{self.price})"
