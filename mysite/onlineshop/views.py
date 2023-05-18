from django.shortcuts import render
from .models import Product, Order
from django .shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def search(request):
    query = request.GET.get('query')
    search_results = Product.objects.filter(Q(name__icontains=query) | Q(price__icontains=query))
    return render(request, 'search.html', {'products': search_results, 'query': query})

# Create your views here.
def products(request):
    paginator = Paginator(Product.objects.all(), 6)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    context = {
        "products": paged_products,
    }
    return render(request, "products.html", context=context)

def product(request, product_id):
    context = {
        "product": get_object_or_404(Product, pk=product_id)
    }
    return render(request, 'product.html', context=context)

class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = 'orders'
    paginate_by = 4

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = 'order'

from django.contrib.auth import get_user_model

class MyOrderListView(generic.ListView):
    model = Order
    template_name = 'my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        User = get_user_model()
        customer = User.objects.get(username=self.request.user.username).customer
        return Order.objects.filter(customer=customer)

