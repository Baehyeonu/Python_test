from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Command(BaseCommand):
    help = '샘플 상품을 생성합니다'

    def handle(self, *args, **kwargs):
        # 테스트 사용자 확인
        try:
            user = User.objects.get(email='test@example.com')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ 테스트 사용자가 없습니다.'))
            self.stdout.write(self.style.ERROR('   먼저 "python manage.py create_test_user"를 실행하세요.'))
            return

        # 샘플 상품 생성
        if Product.objects.count() == 0:
            sample_products = [
                {
                    'user': user,
                    'name': '클래식 티셔츠',
                    'description': '편안하고 스타일리시한 클래식 티셔츠입니다.',
                    'price': 29000,
                    'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
                    'stock': 100,
                    'category': 'clothing'
                },
                {
                    'user': user,
                    'name': '모던 진',
                    'description': '고품질 모던 핏 청바지입니다.',
                    'price': 89000,
                    'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                    'stock': 50,
                    'category': 'clothing'
                },
                {
                    'user': user,
                    'name': '러닝 슈즈',
                    'description': '가볍고 편안한 러닝화입니다.',
                    'price': 129000,
                    'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
                    'stock': 75,
                    'category': 'shoes'
                },
                {
                    'user': user,
                    'name': '가죽 지갑',
                    'description': '고급 가죽으로 만든 지갑입니다.',
                    'price': 59000,
                    'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=400',
                    'stock': 30,
                    'category': 'accessories'
                },
                {
                    'user': user,
                    'name': '스마트 워치',
                    'description': '최신 기능을 갖춘 스마트 워치입니다.',
                    'price': 199000,
                    'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
                    'stock': 25,
                    'category': 'accessories'
                },
                {
                    'user': user,
                    'name': '캐주얼 스니커즈',
                    'description': '일상에서 편안하게 신을 수 있는 스니커즈입니다.',
                    'price': 79000,
                    'image_url': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400',
                    'stock': 60,
                    'category': 'shoes'
                }
            ]

            for product_data in sample_products:
                Product.objects.create(**product_data)
            
            self.stdout.write(self.style.SUCCESS(f'✓ {len(sample_products)}개의 샘플 상품 생성 완료'))
        else:
            self.stdout.write(self.style.WARNING('샘플 상품이 이미 존재합니다'))

