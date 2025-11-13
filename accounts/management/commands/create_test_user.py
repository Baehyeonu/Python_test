from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = '테스트 사용자를 생성합니다'

    def handle(self, *args, **kwargs):
        # 테스트 사용자 생성
        if not User.objects.filter(email='test@example.com').exists():
            user = User.objects.create_user(
                email='test@example.com',
                password='test1234',
                name='Test User'
            )
            self.stdout.write(self.style.SUCCESS('✓ 테스트 사용자 생성 완료'))
            self.stdout.write(self.style.SUCCESS(f'   이메일: {user.email}'))
            self.stdout.write(self.style.SUCCESS('   비밀번호: test1234'))
        else:
            self.stdout.write(self.style.WARNING('테스트 사용자가 이미 존재합니다'))

