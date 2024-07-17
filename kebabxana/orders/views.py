from django.db import transaction
from django.forms import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView
from django.urls import reverse_lazy

from .forms import CreateOrderForm
from .models import Order, OrderDetail
from cart.models import Cart
from kebab.utils import DataMixin
from users.models import User

class CreateOrderView(LoginRequiredMixin, FormView, DataMixin):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:profile')
    title_page = 'Оформить заказ'

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['phone_number'] = self.request.user.phone_number
        return initial
    
    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    # Создать заказ
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                        comment=form.cleaned_data['comment'],
                    )
                    # Создать заказанные товары
                    for cart_item in cart_items:
                        product=cart_item.product
                        name=cart_item.product.product_name
                        price=cart_item.product.product_price
                        quantity=cart_item.quantity

                        OrderDetail.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )

                    cart_items.delete()
                    user.first_name = form.cleaned_data['first_name']
                    user.phone_number = form.cleaned_data['phone_number']
                    user.save()
                    return redirect('users:profile')
        except ValidationError as e:
            return redirect('orders:create_order')