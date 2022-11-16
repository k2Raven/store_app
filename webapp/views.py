from django.shortcuts import render, get_object_or_404
from webapp.models import Product


# Create your views here.
def index_view(request):
    products = Product.objects.filter(balance__gt=0).order_by('category', 'name')
    return render(request, 'index.html', {'products': products})


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_view.html', {'product': product})
