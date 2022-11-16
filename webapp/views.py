from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Product, CATEGORIES_CHOICES
from webapp.forms import SearchForm, ProductForm


# Create your views here.
def index_view(request):
    products = Product.objects.filter(balance__gt=0).order_by('category', 'name')
    form = ProductForm()
    search_form = SearchForm(data=request.GET)
    if search_form.is_valid():
        name = search_form.cleaned_data['search']
        if name:
            products = products.filter(name=name)
            # products = products.filter(name__icontains=name)

    return render(request, 'index.html',
                  {'products': products, 'form': form, 'search_form': search_form, 'categories': CATEGORIES_CHOICES})


def product_by_category_view(request, category, ):
    products = Product.objects.filter(balance__gt=0, category=category).order_by('name')
    form = ProductForm()
    search_form = SearchForm(data=request.GET)
    if search_form.is_valid():
        name = search_form.cleaned_data['search']
        if name:
            products = products.filter(name=name)
            # products = products.filter(name__icontains=name)
    try:
        name_category = dict(CATEGORIES_CHOICES)[category]
    except KeyError:
        raise Http404()
    return render(request, 'product_by_category.html',
                  {'products': products, 'form': form, 'search_form': search_form, 'category': name_category})


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_view.html', {'product': product})


def product_create_view(request):
    if request.method == "POST":
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(**form.cleaned_data)
            return redirect('product_view', pk=product.pk)
        else:
            products = Product.objects.filter(balance__gt=0).order_by('category', 'name')
            search_form = SearchForm(data=request.GET)
            if search_form.is_valid():
                name = search_form.cleaned_data['search']
                if name:
                    products = products.filter(name=name)
            return render(request, 'index.html', {'products': products, 'form': form, 'search_form': search_form,
                                                  'categories': CATEGORIES_CHOICES})


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'balance': product.balance,
            'price': product.price,
        })
        return render(request, 'product_create.html', {'form': form, 'product': product})
    elif request.method == "POST":
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.balance = form.cleaned_data['balance']
            product.price = form.cleaned_data['price']
            product.save()
            return redirect('product_view', pk=product.pk)
        return render(request, 'product_update.html', {'form': form})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        return render(request, 'product_delete.html', {'product': product})
    elif request.method == "POST":
        product.delete()
        return redirect('index')
