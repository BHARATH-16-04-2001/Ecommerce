from . import views
from django.urls import path

urlpatterns = [
  path('', views.cart, name="cart"),
  path('add/', views.cart_add, name="cart_add"),
  path('delete/', views.cart_delete, name="cart_delete"),
  path('update/', views.cart_update, name="cart_update"),

]
