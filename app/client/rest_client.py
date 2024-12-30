import requests
import json

def run():
    base_url = "http://localhost:8000"
    
    # 创建用户
    user_data = {
        "id": 2,
        "name": "李四",
        "email": "lisi@example.com",
        "user_type": "NORMAL",
        "phone_numbers": ["123-456-7890"],
        "address": {
            "street": "南京路456号",
            "city": "上海",
            "country": "中国"
        }
    }
    
    print("=== 创建用户 ===")
    response = requests.post(f"{base_url}/users", json=user_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    print("\n=== 获取用户 ===")
    response = requests.get(f"{base_url}/users/2")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

if __name__ == '__main__':
    run() 