from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """ A view to display single product details page """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_details.html', context)


def services(request):
    """ A view to display all of the services"""
    services = Product.objects.filter(is_a_service=True)
    context = {
        'services': services,
    }

    return render(request, 'products/services.html', context)


def service_details(request, service_id):
    """ A view to display single service details page """
    all_services = Product.objects.filter(is_a_service=True)
    service = get_object_or_404(all_services, pk=service_id)
    context = {
        'service': service,
    }

    return render(request, 'products/service_details.html', context)
