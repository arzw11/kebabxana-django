from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import Category, Products
from .utils import DataMixin


class KebabHome(DataMixin,ListView):
    model = Category
    template_name = "kebab/index.html"
    context_object_name = 'cats'
    title_page = "КебабХана"
    
def about(request):
    return render(request, 'kebab/about.html')
    
    
