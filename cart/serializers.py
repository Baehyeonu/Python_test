from rest_framework import serializers
from .models import Cart
from products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    """장바구니 시리얼라이저"""
    
    product = ProductSerializer(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    cart_id = serializers.IntegerField(source='id', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    
    class Meta:
        model = Cart
        fields = (
            'cart_id',
            'product_id',
            'product',
            'quantity',
            'total_price',
            'created_at'
        )
        read_only_fields = ('cart_id', 'product_id', 'total_price', 'created_at')


class AddToCartSerializer(serializers.Serializer):
    """장바구니 추가 시리얼라이저"""
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1, min_value=1)
    
    def validate_quantity(self, value):
        """수량 유효성 검사"""
        if value < 1:
            raise serializers.ValidationError('수량은 1개 이상이어야 합니다.')
        return value


class UpdateCartSerializer(serializers.Serializer):
    """장바구니 수량 수정 시리얼라이저"""
    quantity = serializers.IntegerField(required=True, min_value=1)
    
    def validate_quantity(self, value):
        """수량 유효성 검사"""
        if value < 1:
            raise serializers.ValidationError('올바른 수량을 입력해주세요.')
        return value

