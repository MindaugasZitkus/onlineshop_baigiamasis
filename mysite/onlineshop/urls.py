from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from . import views



urlpatterns = [
    path('', views.products, name="products"),
    path('products/<int:product_id>', views.product, name="product"),
    path('orders/', views.OrderListView.as_view(), name="orders"),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="order"),
    path('search/', views.search, name='search'),
    path('myorders/', views.MyOrderListView.as_view(), name="myorders"),
    path('cart/', views.cart, name="cart"),
    path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('checkout/', views.checkout, name="checkout"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
