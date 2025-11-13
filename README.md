# Django Backend API

이 프로젝트는 JavaScript(Express)에서 Python(Django)로 변환된 백엔드 API입니다.

## 기술 스택

- Python 3.10+
- Django 5.0
- Django REST Framework
- MySQL
- JWT Authentication

## 설치 방법

### 1. 가상환경 생성 및 활성화

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env.example` 파일을 `.env`로 복사하고 필요한 값을 설정하세요.

```bash
cp .env.example .env
```

### 4. 데이터베이스 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 초기 데이터 로드 (선택사항)

```bash
# 관리자 계정 생성
python manage.py createsuperuser

# 샘플 데이터 로드
python manage.py loaddata fixtures/initial_data.json
```

### 6. 서버 실행

```bash
python manage.py runserver 3001
```

서버는 `http://localhost:3001`에서 실행됩니다.

## API 엔드포인트

### 인증 (Auth)
- `POST /api/auth/signup` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/auth/profile` - 사용자 프로필 조회 (인증 필요)

### 상품 (Products)
- `GET /api/products/` - 상품 목록 조회
- `GET /api/products/{id}/` - 상품 상세 조회
- `POST /api/products/` - 상품 생성 (인증 필요)
- `PUT /api/products/{id}/` - 상품 수정 (인증 필요, 등록자만)
- `DELETE /api/products/{id}/` - 상품 삭제 (인증 필요, 등록자만)

### 장바구니 (Cart)
- `GET /api/cart/` - 장바구니 조회 (인증 필요)
- `POST /api/cart/add` - 장바구니에 상품 추가 (인증 필요)
- `PUT /api/cart/{product_id}/update` - 장바구니 수량 수정 (인증 필요)
- `DELETE /api/cart/{product_id}` - 장바구니에서 상품 제거 (인증 필요)
- `DELETE /api/cart/clear` - 장바구니 비우기 (인증 필요)

## 관리자 페이지

Django 관리자 페이지는 `/admin/`에서 접근할 수 있습니다.

```bash
# 슈퍼유저 생성
python manage.py createsuperuser
```

## 개발 명령어

```bash
# 마이그레이션 파일 생성
python manage.py makemigrations

# 마이그레이션 실행
python manage.py migrate

# Django shell 실행
python manage.py shell

# 테스트 실행
python manage.py test
```

## 주요 변경사항

JavaScript(Express)에서 Python(Django)로의 주요 변경사항:

1. **라우팅**: Express 라우터 → Django URL patterns
2. **컨트롤러**: Express controllers → Django views/viewsets
3. **서비스**: Express services → Django models + serializers
4. **미들웨어**: Express middleware → Django middleware + permissions
5. **ORM**: mysql2 → Django ORM
6. **인증**: JWT (jsonwebtoken) → djangorestframework-simplejwt

## 문제 해결

### MySQL 연결 오류
- MySQL이 실행 중인지 확인하세요
- `.env` 파일의 데이터베이스 설정을 확인하세요

### mysqlclient 설치 오류
macOS에서 mysqlclient 설치 시 오류가 발생하면:

```bash
brew install mysql
pip install mysqlclient
```

## 라이선스

MIT

