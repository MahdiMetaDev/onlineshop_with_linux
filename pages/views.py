from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.contrib import messages


class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        messages.error(request, _("This page is not ready to use!"))    
        return super().get(request, *args, **kwargs)


class AboutUsPageView(TemplateView):
    template_name = "pages/aboutus.html"

    def get(self, request, *args, **kwargs):
        messages.error(request, _("This page is not ready to use!"))    
        return super().get(request, *args, **kwargs)
