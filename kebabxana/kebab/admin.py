from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Products, Category

admin.site.site_header = 'КебабХана — админка'
admin.site.index_title = 'КебабХана'

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'categories', 'is_active']
    list_display_links = ['id', 'product_name']

    readonly_fields = ['show_photo']

    ordering = ['categories', 'product_price']
    
    search_fields = ['product_name__startswith']
    list_filter = ['categories__name', 'is_active']
    
    prepopulated_fields = {'slug': ('product_name',)}

    actions = ['set_active', 'set_inactive']

    @admin.display(description='Изображение')
    def show_photo(self, product:Products):
        return mark_safe(f'<img src="{product.product_images.url}" width=100>')

    @admin.action(description='Выставить на продажу.')
    def set_active(self, request, queryset):
        count = queryset.update(is_active=Products.Status.ACTIVE)
        self.message_user(request, f'Выставлен(о) {count} товар(ов) на продажу.')
    
    @admin.action(description='Снять с продажи.')
    def set_inactive(self, request, queryset):
        count = queryset.update(is_active=Products.Status.INACTIVE)
        self.message_user(request, f'Снят(о) {count} товар(ов) с продажи.', messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    
    ordering = ['id']

    prepopulated_fields = {'slug': ('name',)}