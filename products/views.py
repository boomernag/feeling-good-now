from django.shortcuts import render, redirect, reverse, \
    get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm, ServiceForm


def all_products(request):
    """ A view to display all of the products with search queries"""

    all_products = Product.objects.filter(is_a_service=False)
    active_products = all_products.filter(discontinued=False)
    # empty query and categories when tha page is loaded
    query = None
    categories = None

    if request.GET:
        # allow to show thr specific categories of products
        if 'category' in request.GET:
            # to split categories into list ar the commas
            categories = request.GET['category'].split(',')
            # the __in syntax allow to search for the name field
            # in categories model
            active_products = active_products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'serach_term_input' in request.GET:
            query = request.GET['serach_term_input']
            # if the query is blank, the error message will be displayed
            if not query:
                messages.error(request,
                               "You didn't enter any search key words!\
                                    Please, try again.")
                return redirect(reverse('products'))
            # if query is not blank -> ability to search by name OR description
            search_queries = Q(name__icontains=query) | \
                Q(description__icontains=query)
            # pass quieries to the filter method to actually filter products
            active_products = active_products.filter(search_queries)

    context = {
        'products': active_products,
        'selected_categories': categories,
        'search_word': query,
    }
    return render(request, 'products/all_products.html', context)


def product_details(request, product_id):
    """ A view to display single product details page """
    all_products = Product.objects.filter(is_a_service=False)
    product = get_object_or_404(all_products, pk=product_id)
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
    """ A view to display single service details page
    """
    all_services = Product.objects.filter(is_a_service=True)
    service = get_object_or_404(all_services, pk=service_id)

    context = {
        'service': service,
    }
    return render(request, 'products/service_details.html', context)


@login_required
def add_product(request):
    """ A view allowing admin to add a product/service to the store
        Credits: the solution for combining 2 forms
        in one view was found in the Stack Overflow:
        https://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django
    """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied!\
             Only store owners can do that!')
        return redirect(reverse('landing'))
    if request.method == 'POST':
        if 'product' in request.POST:
            product_form = ProductForm(request.POST, request.FILES,
                                       prefix='product')
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.discontinued = False
                product.save()
                messages.success(request, 'Successfully added product!')
                return redirect(reverse('product_details', args=[product.id]))
            else:
                messages.error(request, 'Failed to add product. \
                                Please ensure the form is valid.')
            service_form = ServiceForm(prefix='service')
        elif 'service' in request.POST:
            service_form = ServiceForm(request.POST, request.FILES,
                                       prefix='service')
            if service_form.is_valid():
                service = service_form.save(commit=False)
                service.is_a_service = True
                service.discontinued = False
                service.save()
                messages.success(request, 'Successfully added service!')
                return redirect(reverse('service_details', args=[service.id]))
            else:
                messages.error(request, 'Failed to add service. \
                                Please ensure the form is valid.')
            product_form = ProductForm(prefix='product')
    else:
        product_form = ProductForm(prefix='product')
        service_form = ServiceForm(prefix='service')

    template = 'products/add_product.html'
    context = {
        'product_form': product_form,
        'service_form': service_form,
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ A view to allow only admin to edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied!\
             Only store owners can edit products.')
        return redirect(reverse('landing'))
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product.\
                 Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ A view to allow only admin to delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied!\
             Only store owners can delete products.')
        return redirect(reverse('landing'))
    product = get_object_or_404(Product, pk=product_id)
    product.discontinued = True
    product.save()
    messages.info(request, f'{product.name} was successfully deleted.')
    return redirect(reverse('products'))


@login_required
def edit_service(request, service_id):
    """ A view to allow only admin to edit a service in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied!\
             Only store owners can edit services.')
        return redirect(reverse('landing'))
    service = get_object_or_404(Product, pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            service.is_a_service = True
            service.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('service_details', args=[service.id]))
        else:
            messages.error(request, 'Failed to update product.\
                 Please ensure the form is valid.')
    else:
        form = ServiceForm(instance=service)
        messages.info(request, f'You are editing {service.name}')

    template = 'products/edit_service.html'
    context = {
        'form': form,
        'service': service,
    }
    return render(request, template, context)


@login_required
def delete_service(request, service_id):
    """ A view to allow only admin to delete a service from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied!\
             Only store owners can delete services.')
        return redirect(reverse('landing'))
    service = get_object_or_404(Product, pk=service_id)
    service.discontinued = True
    service.save()
    messages.info(request, f'{service.name} was successfully deleted.')
    return redirect(reverse('services'))

