from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import Product
from .serializers import ProductSerializer, ProductCreateUpdateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """상품 ViewSet"""
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """액션에 따라 다른 시리얼라이저 사용"""
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer
    
    def list(self, request):
        """상품 목록 조회 (페이지네이션 적용)"""
        try:
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 10))
            
            products = Product.objects.all().order_by('-created_at')
            
            paginator = Paginator(products, limit)
            page_obj = paginator.get_page(page)
            
            serializer = self.get_serializer(page_obj, many=True)
            
            return Response({
                'products': serializer.data,
                'totalPages': paginator.num_pages,
                'currentPage': page,
                'totalProducts': paginator.count
            })
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request):
        """상품 생성"""
        try:
            # 필수 필드 검증
            if 'name' not in request.data or 'price' not in request.data or 'stock' not in request.data:
                return Response(
                    {'message': 'Name, price, and stock are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # 상품 생성 시 현재 사용자를 등록자로 설정
            product = serializer.save(user=request.user)
            
            return Response(
                {
                    'productId': product.id,
                    'message': 'Product created successfully'
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """상품 상세 조회"""
        try:
            product = self.get_object()
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(
                {'message': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, pk=None):
        """상품 수정"""
        try:
            product = self.get_object()
            
            # 권한 확인: 상품 등록자만 수정 가능
            if product.user != request.user:
                return Response(
                    {'message': 'User not authorized'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = self.get_serializer(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # 전체 상품 정보 반환
            product_serializer = ProductSerializer(product)
            return Response(product_serializer.data)
        except Product.DoesNotExist:
            return Response(
                {'message': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, pk=None):
        """상품 삭제"""
        try:
            product = self.get_object()
            
            # 권한 확인: 상품 등록자만 삭제 가능
            if product.user != request.user:
                return Response(
                    {'message': 'User not authorized'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            product.delete()
            return Response(
                {'message': 'Product deleted successfully'},
                status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            return Response(
                {'message': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

