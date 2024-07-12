from django.template.loader import render_to_string

from cart.models import Cart
from cart.utils import get_user_carts


class CartMixin:
    def get_cart(self, request, product=None, cart_id=None):

        if request.user.is_authenticated:
            query_kwargs = {'user': request.user}
        else:
            query_kwargs = {'session_key': request.session.session_key}

        if product:
            query_kwargs['product'] = product
        if cart_id:
            query_kwargs['id'] = cart_id

        return Cart.objects.filter(**query_kwargs).first()
    
    def render_cart(self, request):
        user_cart = get_user_carts(request)
        cart_items_html = render_to_string(
        'cart/includes/cart_content.html', {'carts': user_cart}, request=request
        )

        return cart_items_html