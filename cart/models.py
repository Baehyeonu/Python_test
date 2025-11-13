from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    """장바구니 모델"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='사용자'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='상품'
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name='수량'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='추가일'
    )
    
    class Meta:
        db_table = 'cart'
        verbose_name = '장바구니'
        verbose_name_plural = '장바구니'
        unique_together = [['user', 'product']]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.quantity}개)"
    
    @property
    def total_price(self):
        """총 가격 계산"""
        return self.product.price * self.quantity

