from django.shortcuts import render, get_object_or_404

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
        "callback_url": "127.0.0.1:8000",
    }

    zp_response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data),
                 headers=request_header)

    data = zp_response.json()["data"]
    authority = data["authority"]
    order.zarinpal_authority = authority
    order.save()
    