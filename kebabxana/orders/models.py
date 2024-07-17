from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from kebab.models import Products
from users.models import User

class OrderDetailQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.product_price() for cart in self)
    
    def total_quantity(self):
        return sum(cart.quantity for cart in self)



class Status(models.Model):
    name = models.CharField(verbose_name='Статус', db_index=True)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статус заказа'
    
    def __str__(self):
        return self.name
    
    

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name='Пользователь', default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    phone_number = PhoneNumberField(region='RU')
    requires_delivery = models.BooleanField(default=False, verbose_name='Требуется доставка')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получении')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    comment = models.TextField(default=None, blank=True, null=True, verbose_name='Комментарий к заказу')
    status = models.ForeignKey(to='Status',on_delete=models.DO_NOTHING, default=Status.objects.get(id=1).pk, verbose_name='Статус заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.phone_number}"


class OrderDetail(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='order_items')
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name='Продукт', default=None)
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    objects = OrderDetailQueryset.as_manager()

    class Meta:
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказа'

    def product_price(self):
        return round(self.product.product_price * self.quantity, 2)
    
    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"