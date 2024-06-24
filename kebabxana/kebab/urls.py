from django.urls import path
from . import views


urlpatterns = [
    path('', views.KebabHome.as_view(), name='home'),
    path('about/', views.about, name='about'),

]
