import grpc
from concurrent import futures
from app.generated import user_pb2
from app.generated import user_pb2_grpc
import os

class UserServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        # 模拟数据库
        self.users = {}
        
    def GetUser(self, request, context):
        user_id = request.user_id
        if user_id not in self.users:
            return user_pb2.UserResponse(
                success=False,
                message=f"User {user_id} not found"
            )
        
        return user_pb2.UserResponse(
            success=True,
            message="User found",
            user=self.users[user_id]
        )
    
    def CreateUser(self, request, context):
        user = request.user
        if user.id in self.users:
            return user_pb2.UserResponse(
                success=False,
                message=f"User {user.id} already exists"
            )
        
        self.users[user.id] = user
        return user_pb2.UserResponse(
            success=True,
            message="User created successfully",
            user=user
        )

def serve():
    # 读取证书文件
    with open('certs/server.key', 'rb') as f:
        private_key = f.read()
    with open('certs/server.crt', 'rb') as f:
        certificate_chain = f.read()

    # 创建服务器证书
    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)]
    )

    # 创建服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    
    # 使用安全证书绑定端口
    server.add_secure_port('[::]:50051', server_credentials)
    print("Secure gRPC server starting on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 