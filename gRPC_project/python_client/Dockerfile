# Python 기본 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY . .

# 필요한 패키지 설치
RUN pip install --no-cache-dir grpcio grpcio-tools

# 실행 명령어
CMD ["python3", "client.py"]
