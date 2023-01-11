from django.urls import reverse_lazy, reverse
from django.views.generic import View, DeleteView, CreateView, TemplateView, ListView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from webapp.models import Product, Order, OrderProduct
from webapp.forms import OrderForm


class AddItemToCart(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        qty = int(request.POST.get('qty'))
        cart = request.session.get('cart', {}) # { '1': 2,  }



        cart_qty = cart.get(str(product.pk), 0)

        if product.balance >= cart_qty + qty:
            cart[str(product.pk)] = cart_qty + qty
            request.session['cart'] = cart


        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('index')


class CartList(TemplateView):
    template_name = 'cart/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        cart = self.request.session.get('cart', {})
        products = [] # [ {'product': product, 'qty': qty, 'total': product.price * qty},  ]
        total = 0

        for pk, qty in cart.items():
            product = get_object_or_404(Product, pk=pk)
            product_total = product.price * qty
            total += product_total
            products.append( {'product': product, 'qty': qty, 'product_total': product_total},)


        context['products'] = products
        context['total'] = total
        context['form'] = OrderForm
        return context


class CartDelete(View):
    def get(self, request, pk,  *args, **kwargs):
        cart = request.session.get('cart', {})
        if pk in cart:
            cart.pop(pk)
            request.session['cart'] = cart
        return redirect('cart_index')




class CartDeleteOne(View):
    def get(self, request, pk,  *args, **kwargs):
        cart = request.session.get('cart', {})
        if pk in cart:
            if cart[pk] > 1:
                cart[pk] -= 1
            else:
                cart.pop(pk)
            request.session['cart'] = cart
        return redirect('cart_index')


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        order = form.save()
        if self.request.user.is_authenticated:
            order.user = self.request.user
            order.save()

        cart = self.request.session.get('cart', {})

        for pk, qty in cart.items():
            product = get_object_or_404(Product, pk=pk)
            OrderProduct.objects.create(product=product, qty=qty, order=order)
            product.balance -= qty
            product.save()

        self.request.session.pop('cart')

        return redirect(self.success_url)


class OrderList(LoginRequiredMixin, ListView):
    template_name = 'cart/order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


