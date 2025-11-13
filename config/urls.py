"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({'message': 'Hello from the backend!'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/auth/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
]

