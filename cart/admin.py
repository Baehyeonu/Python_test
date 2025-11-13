from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'get_total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'product__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'get_total_price')
    
    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = '총 가격'

