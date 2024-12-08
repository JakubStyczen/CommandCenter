from django.shortcuts import render
from .models import Product

# Read View
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'TestApp/product_list.html', {'products':products})
