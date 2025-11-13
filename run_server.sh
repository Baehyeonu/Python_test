#!/bin/bash

# Django 서버 실행 스크립트

echo "🚀 Django 서버를 시작합니다..."
echo ""

# 마이그레이션 확인
if [ ! -f "db.sqlite3" ]; then
    echo "📦 데이터베이스 마이그레이션 실행 중..."
    python manage.py makemigrations
    python manage.py migrate
    echo ""
    
    echo "📝 초기 데이터 생성 중..."
    python manage.py setup_initial_data
    echo ""
fi

# 서버 실행
echo "✅ 서버를 포트 3001에서 실행합니다..."
python manage.py runserver 3001

