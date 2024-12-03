package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"sync"
	"time"

	pb "grpc_project/proto"

	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedTargetServiceServer
	mu           sync.Mutex
	requestCount int
}

func (s *server) SendRequest(ctx context.Context, req *pb.RequestMessage) (*pb.ResponseMessage, error) {
	start := time.Now()

	s.mu.Lock()
	s.requestCount++
	requestID := s.requestCount
	s.mu.Unlock()

	log.Printf("Request #%d received at %s: %s", requestID, time.Now().Format(time.RFC3339), req.Message)

	time.Sleep(100 * time.Millisecond)

	duration := time.Since(start)
	log.Printf("request: #%d processed in %v", requestID, duration)

	return &pb.ResponseMessage{Response: fmt.Sprintf("Acknowledged #%d", requestID)}, nil
}

func main() {
	//로그 파일 생성
	logFile, err := os.OpenFile("server.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatalf("Failed to create log file: %v", err)
	}
	defer logFile.Close()

	//로그 출력 설정
	log.SetOutput(logFile)

	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	grpcServer := grpc.NewServer()
	pb.RegisterTargetServiceServer(grpcServer, &server{})

	log.Println("Server is running on port 50051")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
