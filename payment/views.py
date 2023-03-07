from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.utils.translation import gettext as _

import requests
import json

from orders.models import Order


def payment_process(request):
    
    """ connect to zarinpal with merchant-code &
        send user-product-price with redirect url """

    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = "https://api.zarinpal.com/pg/v4/payment/request.json"

    request_header = {
        "accept": "application/json", # return-type -> json format
        "content-type": "application/json", # sent-type -> json format
    }

    request_data = {
        "merchant_id": "[PUT YOUR MERCHANT_ID HERE!!]",
        "amount": rial_total_price,
        "description": f"#{order.id}: {order.user.first_name} {order.user.last_name}",
        "callback_url": reverse("payment:payment_callback"),
    }

    zp_response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data),
                 headers=request_header)

    data = zp_response.json()["data"]
    authority = data["authority"]
    order.zarinpal_authority = authority
    order.save()
    
    if ("errors" not in data) or (len(data["errors"]) == 0):
        return redirect(f"https://www.zarinpal.com/pg/StartPay/{authority}")
    else:
        return HttpResponse("Error from zarinpal occured!")


def payment_callback(request):

    payment_authority = request.GET.get("Authority")
    payment_status = request.GET.get("Status")

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == "OK":

        request_header = {
            "accept": "application/json", # return-type -> json format
            "content-type": "application/json", # sent-type -> json format
        }

        request_data = {
            "merchant_id": "[PUT YOUR MERCHANT_ID HERE!!]",
            "amount": rial_total_price,
            "authority": payment_authority,
        }

        verify_response = requests.post(
            url="https://api.zarinpal.com/pg/v4/payment/verify.json",
            data=json.dumps(request_data),
            headers=request_header,
        )


        if "data" in verify_response.json() and \
            ("errors" not in verify_response.json()["data"] or
            len(verify_response.json()["data"]["errors"]) == 0):

            data = verify_response.json()["data"]
            payment_code = data["code"]

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data["ref_id"]
                order.zarinpal_data = data
                order.save()

                return HttpResponse(_("Your payment has been successfully completed !"))
        
            elif payment_code == 101:
                return HttpResponse(_("This transaction has already been registered"))

            else:
                error_code = verify_response.json()["errors"]["code"]
                error_message = verify_response.json()["errors"]["message"]
                return HttpResponse(_(f"The transaction was unsuccessful {error_code} {error_message}"))
