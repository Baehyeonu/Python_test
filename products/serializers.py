from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """상품 시리얼라이저"""
    
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id',
            'user_id',
            'name',
            'description',
            'price',
            'image_url',
            'stock',
            'category',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'user_id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        """상품 생성 시 현재 사용자를 등록자로 설정"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """상품 생성/수정 시리얼라이저"""
    
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image_url', 'stock', 'category')
    
    def validate_price(self, value):
        """가격 유효성 검사"""
        if value < 0:
            raise serializers.ValidationError('가격은 0보다 커야 합니다.')
        return value
    
    def validate_stock(self, value):
        """재고 유효성 검사"""
        if value < 0:
            raise serializers.ValidationError('재고는 0보다 크거나 같아야 합니다.')
        return value

