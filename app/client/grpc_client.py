import grpc
from app.generated import user_pb2
from app.generated import user_pb2_grpc

def run():
    # 读取证书
    with open('certs/server.crt', 'rb') as f:
        root_certificates = f.read()
    
    # 创建证书凭据
    credentials = grpc.ssl_channel_credentials(root_certificates)
    
    # 创建安全的 channel
    with grpc.secure_channel('localhost:50051', credentials) as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        
        # 创建用户
        user = user_pb2.User(
            id=1,
            name="张三",
            email="zhangsan@example.com",
            user_type=user_pb2.User.ADMIN,
            phone_numbers=["123-456-7890", "098-765-4321"],
            address=user_pb2.User.Address(
                street="中山路123号",
                city="北京",
                country="中国"
            )
        )
        
        print("=== 创建用户 ===")
        response = stub.CreateUser(user_pb2.CreateUserRequest(user=user))
        print(f"响应: {response.message}")
        
        print("\n=== 获取用户 ===")
        response = stub.GetUser(user_pb2.GetUserRequest(user_id=1))
        if response.success:
            user = response.user
            print(f"用户信息:")
            print(f"ID: {user.id}")
            print(f"姓名: {user.name}")
            print(f"邮箱: {user.email}")
            print(f"用户类型: {user_pb2.User.UserType.Name(user.user_type)}")
            print(f"电话号码: {', '.join(user.phone_numbers)}")
            print(f"地址: {user.address.country} {user.address.city} {user.address.street}")

if __name__ == '__main__':
    run() 