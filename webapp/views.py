from django.shortcuts import render, get_object_or_404
from webapp.models import Product
from webapp.forms import SearchForm


# Create your views here.
def index_view(request):
    products = Product.objects.filter(balance__gt=0).order_by('category', 'name')
    form = SearchForm(data=request.GET)
    if form.is_valid():
        name = form.cleaned_data['search']
        if name:
            products = products.filter(name=name)
            # products = products.filter(name__icontains=name)

    return render(request, 'index.html', {'products': products, 'form': form})


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_view.html', {'product': product})
