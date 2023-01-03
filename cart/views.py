from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.contrib import messages

from products.models import Product
from .cart import Cart
from .forms import AddToCartProductForm


def cart_detail_view(request):

    """ show products in the cart for payment """

    cart = Cart(request)

    for item in cart:
        item["product_update_quantity_form"] = AddToCartProductForm(initial={
            "quantity": item["quantity"],
            "inplace": True,
        })
    
    return render(request, "cart/cart_detail.html", {
        "cart": cart,
    })


@require_POST
def add_to_cart_view(request, product_id):

    """ get product and its quantity from request.POST and add it to
    cart then redirect to cart_detail """

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    form = AddToCartProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        print(cleaned_data)
        quantity = cleaned_data["quantity"]

        cart.add(product, quantity, replace_current_quantity=cleaned_data["inplace"])
    
    messages.success(request, _("The product added to cart successfully!"))

    return redirect("cart:cart_detail")


def remove_from_cart(request, product_id):

    """ remove a product from the cart """

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    
    cart.remove(product)

    if not cart:
        messages.error(request, _(
            "The cart is empty, please go to product list and add your favorite product \
            to the cart"
        ))
    else:
        messages.warning(request, _("The product removed successfully!"))

    return redirect("cart:cart_detail")


def clear_the_cart(request):

    """ clear the cart totally """

    cart = Cart(request)

    cart.clear()

    messages.error(request, _(
        "The cart is empty, please go to product list and add your favorite product \
        to the cart"
    ))

    return redirect("cart:cart_detail")
