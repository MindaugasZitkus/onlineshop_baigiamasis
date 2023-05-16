from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.products, name="products"),
    path('products/<int:product_id>', views.product, name="product"),
    path('orders/', views.OrderListView.as_view(), name="orders"),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="order"),
]