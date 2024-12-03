FROM golang:1.23-alpine

WORKDIR /app

# 필요한 파일만 복사하여 go mod tidy 실행
COPY go.mod go.sum ./
RUN go mod tidy

# 나머지 소스 파일 복사 및 빌드
COPY . .
RUN go build -o grpc-server main.go

EXPOSE 50051

CMD ["./grpc-server"]
