from django.urls import reverse_lazy
from django.views.generic import View, ListView, DeleteView
from django.shortcuts import redirect, get_object_or_404

from webapp.models import Product, Cart


class AddItemToCart(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))

        try:
            cart = Cart.objects.get(product=product)
            if cart.qty < product.balance:
                cart.qty += 1
                cart.save()
        except Cart.DoesNotExist:
            if product.balance > 0:
                Cart.objects.create(product=product, qty=1)

        return redirect('index')


class CartList(ListView):
    model = Cart
    template_name = 'cart/index.html'
    context_object_name = "carts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        total = 0
        for cart in self.model.objects.all():
            total += cart.get_product_total()
        context['total'] = total
        return context


class CartDelete(DeleteView):
    model = Cart
    success_url = reverse_lazy('cart_index')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
