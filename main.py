from user_pb2 import User
import json

def create_user():
    # 创建一个新的 User 消息
    user = User()
    user.id = 1
    user.name = "张三"
    user.email = "zhangsan@example.com"
    user.user_type = User.ADMIN
    
    # 添加电话号码
    user.phone_numbers.append("123-456-7890")
    user.phone_numbers.append("098-765-4321")
    
    # 设置地址
    user.address.street = "中山路123号"
    user.address.city = "北京"
    user.address.country = "中国"
    
    return user

def user_to_dict(user):
    """将 User protobuf 对象转换为 Python 字典"""
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'user_type': User.UserType.Name(user.user_type),
        'phone_numbers': list(user.phone_numbers),
        'address': {
            'street': user.address.street,
            'city': user.address.city,
            'country': user.address.country
        }
    }

def main():
    # 创建用户
    user = create_user()
    
    # Protobuf 序列化
    protobuf_data = user.SerializeToString()
    protobuf_size = len(protobuf_data)
    
    # JSON 序列化
    json_data = json.dumps(user_to_dict(user), ensure_ascii=False).encode('utf-8')
    json_size = len(json_data)
    
    # 打印大小对比
    print("\n=== 序列化大小对比 ===")
    print(f"Protobuf 大小: {protobuf_size} 字节")
    print(f"JSON 大小: {json_size} 字节")
    print(f"Protobuf 相比 JSON 节省: {(json_size - protobuf_size) / json_size * 100:.2f}%")
    
    # 打印 JSON 内容（方便查看）
    print("\n=== JSON 格式内容 ===")
    print(json_data.decode('utf-8'))
    
    # 反序列化并打印用户信息
    print("\n=== Protobuf 反序列化后的用户信息 ===")
    deserialized_user = User()
    deserialized_user.ParseFromString(protobuf_data)
    print(f"ID: {deserialized_user.id}")
    print(f"姓名: {deserialized_user.name}")
    print(f"邮箱: {deserialized_user.email}")
    print(f"用户类型: {User.UserType.Name(deserialized_user.user_type)}")
    print(f"电话号码: {', '.join(deserialized_user.phone_numbers)}")
    print(f"地址: {deserialized_user.address.country} {deserialized_user.address.city} {deserialized_user.address.street}")

if __name__ == "__main__":
    main() 