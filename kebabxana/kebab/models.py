from django.db import models

class ActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=Products.Status.ACTIVE)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Products(models.Model):
    class Status(models.IntegerChoices):
        INACTIVE = 0, 'Склад'
        ACTIVE = 1, 'Продажа'

    product_name = models.CharField(max_length=100, verbose_name='Название')
    product_price = models.IntegerField(null=False, default=0, verbose_name='Цена')
    product_images = models.ImageField(upload_to='kebab/images/',null=True, verbose_name='Иллюстрация')
    categories = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    is_active = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.INACTIVE, verbose_name="Статус")

    objects = models.Manager()
    active = ActivityManager()

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = 'Позиция меню'
        verbose_name_plural = 'Позиции меню'
        ordering = ['categories', 'product_price']
