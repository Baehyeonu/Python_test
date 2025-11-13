from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'user', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'description', 'category')
        }),
        ('가격 및 재고', {
            'fields': ('price', 'stock')
        }),
        ('이미지', {
            'fields': ('image_url',)
        }),
        ('등록자', {
            'fields': ('user',)
        }),
        ('날짜 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

