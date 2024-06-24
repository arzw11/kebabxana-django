from django import template

from kebab.models import Products

register = template.Library()

@register.simple_tag()
def get_products():
    return Products.active.all()