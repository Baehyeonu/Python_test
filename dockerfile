# 1. 사용할 기본 이미지(Base Image) 정의
FROM python:3.11-slim

# 2. 컨테이너 내부의 작업 디렉토리 설정
WORKDIR /app

# 3. 애플리케이션의 의존성 파일(requirements.txt)을 컨테이너에 복사
# 먼저 복사해서 캐싱 효율을 높입니다.
COPY requirements.txt .

# 4. 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 프로젝트 파일들을 컨테이너에 복사
COPY . .

# 6. 서버 애플리케이션이 실행될 포트 노출 (예: Flask 기본 포트 5000)
EXPOSE 5000

# 7. 컨테이너가 시작될 때 실행할 명령어 (서버 시작 명령어)
# 예: gunicorn (프로덕션용 WSGI 서버)을 사용하는 경우
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
# 예: 단순 Flask 개발 서버인 경우
# CMD ["python", "app.py"]
