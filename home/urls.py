from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact_view, name="contact"),
    path("success/", TemplateView.as_view(template_name="contact/success.html"), name="success"),
    path("download/brochure/", views.download_brochure, name="download_brochure"),
]
