from django.shortcuts import render
from .models import Product

# Create your views here.
def products(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, "products.html", context=context)