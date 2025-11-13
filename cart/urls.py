from django.urls import path
from .views import CartViewSet

app_name = 'cart'

urlpatterns = [
    path('', CartViewSet.as_view({'get': 'list'}), name='cart-list'),
    path('add', CartViewSet.as_view({'post': 'add'}), name='cart-add'),
    path('<int:pk>', CartViewSet.as_view({'delete': 'destroy'}), name='cart-remove'),
    path('<int:pk>/update', CartViewSet.as_view({'put': 'update_quantity'}), name='cart-update'),
    path('clear', CartViewSet.as_view({'delete': 'clear'}), name='cart-clear'),
]

