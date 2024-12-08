from django.shortcuts import render
from . import views
from django.urls import include, path
from .views import contact_view

urlpatterns = [
    path('', views.index),
    path('contact/', contact_view, name='contact'),
    path('success/', lambda request: render(request, 'contact/success.html'), name='success'),
    path('download/brochure/', views.download_brochure, name='download_brochure'),
]