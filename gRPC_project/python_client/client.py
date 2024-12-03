import grpc
import service_pb2
from concurrent.futures import ThreadPoolExecutor
import service_pb2_grpc
import os
import time

def send_request(stub, message):
    try:
        response = stub.SendRequest(service_pb2.RequestMessage(message=message))
        print(f"Response: {response.response}")
    except grpc.RpcError as e:
        print(f"RPC failed: {e.code()} - {e.details()}")

def run():
    server_address = os.getenv("TARGET_SERVER", "grpc-go-service:50051")
    duration =300 #5분동안 지속
    start_time = time.time()

    with grpc.insecure_channel(server_address) as channel:
        stub = service_pb2_grpc.TargetServiceStub(channel)
        while time.time() - start_time < duration:  
            with ThreadPoolExecutor(max_workers=50) as executor:
                for i in range(100): 
                    executor.submit(send_request, stub, f"MEssage: {i}")
            time.sleep(1)

if __name__ == "__main__":
    run()