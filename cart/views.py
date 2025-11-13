from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Cart
from products.models import Product
from .serializers import CartSerializer, AddToCartSerializer, UpdateCartSerializer


class CartViewSet(viewsets.ViewSet):
    """장바구니 ViewSet"""
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """장바구니 조회"""
        try:
            cart_items = Cart.objects.filter(user=request.user).select_related('product')
            serializer = CartSerializer(cart_items, many=True)
            
            # 총 금액 계산
            total_amount = sum(item.total_price for item in cart_items)
            
            return Response({
                'items': serializer.data,
                'totalAmount': float(total_amount),
                'itemCount': len(serializer.data)
            })
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """장바구니에 상품 추가"""
        try:
            serializer = AddToCartSerializer(data=request.data)
            
            # product_id 필수 확인
            if 'productId' not in request.data:
                return Response(
                    {'message': '상품 ID가 필요합니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # productId를 product_id로 변환
            data = {
                'product_id': request.data.get('productId'),
                'quantity': request.data.get('quantity', 1)
            }
            
            serializer = AddToCartSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            # 상품 존재 여부 확인
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {'message': '상품을 찾을 수 없습니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 재고 확인
            if product.stock < quantity:
                return Response(
                    {'message': '재고가 부족합니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 장바구니에 추가 또는 수량 증가
            with transaction.atomic():
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    # 이미 존재하는 경우 수량 증가
                    new_quantity = cart_item.quantity + quantity
                    
                    # 새로운 총 수량이 재고를 초과하는지 확인
                    if product.stock < new_quantity:
                        return Response(
                            {'message': '재고가 부족합니다.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    cart_item.quantity = new_quantity
                    cart_item.save()
            
            return Response(
                {'message': '장바구니에 추가되었습니다.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['put'])
    def update_quantity(self, request, pk=None):
        """장바구니 수량 수정"""
        try:
            serializer = UpdateCartSerializer(data=request.data)
            
            # quantity 필수 확인
            if 'quantity' not in request.data:
                return Response(
                    {'message': '올바른 수량을 입력해주세요.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.is_valid(raise_exception=True)
            quantity = serializer.validated_data['quantity']
            
            # 장바구니 항목 조회 (product_id 기준)
            try:
                cart_item = Cart.objects.get(user=request.user, product_id=pk)
            except Cart.DoesNotExist:
                return Response(
                    {'message': '장바구니 항목을 찾을 수 없습니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 재고 확인
            if cart_item.product.stock < quantity:
                return Response(
                    {'message': '재고가 부족합니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 수량 업데이트
            cart_item.quantity = quantity
            cart_item.save()
            
            return Response(
                {'message': '장바구니가 업데이트되었습니다.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, pk=None):
        """장바구니에서 상품 제거"""
        try:
            # 장바구니 항목 조회 (product_id 기준)
            try:
                cart_item = Cart.objects.get(user=request.user, product_id=pk)
            except Cart.DoesNotExist:
                return Response(
                    {'message': '장바구니 항목을 찾을 수 없습니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart_item.delete()
            
            return Response(
                {'message': '상품이 장바구니에서 제거되었습니다.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """장바구니 비우기"""
        try:
            Cart.objects.filter(user=request.user).delete()
            
            return Response(
                {'message': '장바구니가 비워졌습니다.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

