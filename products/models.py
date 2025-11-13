from django.db import models
from django.conf import settings


class Product(models.Model):
    """상품 모델"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='등록자'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='상품명'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='상품 설명'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='가격'
    )
    image_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='이미지 URL'
    )
    stock = models.IntegerField(
        default=0,
        verbose_name='재고 수량'
    )
    category = models.CharField(
        max_length=100,
        default='general',
        verbose_name='카테고리'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='등록일'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )
    
    class Meta:
        db_table = 'products'
        verbose_name = '상품'
        verbose_name_plural = '상품들'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

