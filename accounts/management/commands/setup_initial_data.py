from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = '초기 데이터를 생성합니다 (테스트 사용자 및 샘플 상품)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('📦 초기 데이터 생성을 시작합니다...\n'))
        
        # 테스트 사용자 생성
        self.stdout.write('1️⃣  테스트 사용자 생성 중...')
        call_command('create_test_user')
        
        self.stdout.write('\n2️⃣  샘플 상품 생성 중...')
        call_command('create_sample_products')
        
        self.stdout.write(self.style.SUCCESS('\n✅ 초기 데이터 설정 완료!'))
        self.stdout.write(self.style.SUCCESS('━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
        self.stdout.write(self.style.SUCCESS('테스트 계정 정보:'))
        self.stdout.write(self.style.SUCCESS('  이메일: test@example.com'))
        self.stdout.write(self.style.SUCCESS('  비밀번호: test1234'))
        self.stdout.write(self.style.SUCCESS('━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))

