from django.shortcuts import render
from django.views import generic

from .models import Product


class ProductListView(generic.ListView):
    model = Product
    
    # will show active products
    queryset = Product.objects.filter(active=True)
    
    template_name = "products/product_list.html"
    context_object_name = "products"
