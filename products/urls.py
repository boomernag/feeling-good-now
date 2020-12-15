from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('services/', views.services, name='services'),
]
