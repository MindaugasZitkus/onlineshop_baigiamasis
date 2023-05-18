from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static, settings

urlpatterns = [
    path('', views.products, name="products"),
    path('products/<int:product_id>', views.product, name="product"),
    path('orders/', views.OrderListView.as_view(), name="orders"),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="order"),
    path('search/', views.search, name='search'),
    path('myorders/', views.MyOrderListView.as_view(), name="myorders"),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
