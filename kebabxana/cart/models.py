from django.db import models

from users.models import User
from kebab.models import Products


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.product_price for cart in self)
    
    def total_quantity(self):
        return sum(cart.quantity for cart in self)

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    

    objects = CartQueryset().as_manager()
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def product_price(self):
        return round(self.product.product_price * self.quantity, 2)

    def __str__(self):
        if self.user:
           return f'Корзина {self.user.username} | Товар {self.product.product_name} | Количество {self.quantity}'
            
        return f'Анонимная корзина | Товар {self.product.product_name} | Количество {self.quantity}'
