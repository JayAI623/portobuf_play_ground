from fastapi import FastAPI, HTTPException
import grpc
from app.generated import user_pb2
from app.generated import user_pb2_grpc
from pydantic import BaseModel
from typing import List, Optional
from app.utils.grpc_client import SecureGrpcClient

app = FastAPI()

# Pydantic models for REST API
class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    id: int
    name: str
    email: str
    user_type: str
    phone_numbers: List[str]
    address: Address

# 使用 SecureGrpcClient
grpc_client = SecureGrpcClient()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        with grpc_client.channel_scope() as stub:
            response = stub.GetUser(user_pb2.GetUserRequest(user_id=user_id))
            if not response.success:
                raise HTTPException(status_code=404, detail=response.message)
            
            return {
                "success": response.success,
                "message": response.message,
                "user": {
                    "id": response.user.id,
                    "name": response.user.name,
                    "email": response.user.email,
                    "user_type": user_pb2.User.UserType.Name(response.user.user_type),
                    "phone_numbers": list(response.user.phone_numbers),
                    "address": {
                        "street": response.user.address.street,
                        "city": response.user.address.city,
                        "country": response.user.address.country
                    }
                }
            }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users")
async def create_user(user: User):
    try:
        with grpc_client.channel_scope() as stub:
            # 转换 REST 请求到 gRPC 请求
            user_type = getattr(user_pb2.User.UserType, user.user_type)
            grpc_user = user_pb2.User(
                id=user.id,
                name=user.name,
                email=user.email,
                user_type=user_type,
                phone_numbers=user.phone_numbers,
                address=user_pb2.User.Address(
                    street=user.address.street,
                    city=user.address.city,
                    country=user.address.country
                )
            )
            
            response = stub.CreateUser(user_pb2.CreateUserRequest(user=grpc_user))
            if not response.success:
                raise HTTPException(status_code=400, detail=response.message)
            
            return {
                "success": response.success,
                "message": response.message
            }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 