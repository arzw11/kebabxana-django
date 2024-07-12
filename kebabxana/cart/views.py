from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import View
from django.template.loader import render_to_string

from .models import Cart
from .mixins import CartMixin
from .utils import get_user_carts
from kebab.models import Products


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Products.active.get(id=product_id)

        cart = self.get_cart(request=request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                product=product, quantity=1)
        response_data = {
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)
    
class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart = Cart.objects.get(id=cart_id)

        cart.delete()

        response_data = {
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)

class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        quantity = request.POST.get('quantity')
        cart = Cart.objects.get(id=cart_id)

        cart.quantity = quantity
        cart.save()

        response_data = {
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)