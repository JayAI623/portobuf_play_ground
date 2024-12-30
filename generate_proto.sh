#!/bin/bash

# 确保目标目录存在
mkdir -p app/generated

# 生成 protobuf 文件
python -m grpc_tools.protoc \
    -I./app/protos \
    --python_out=./app/generated \
    --grpc_python_out=./app/generated \
    ./app/protos/user.proto

# 创建 __init__.py 文件
touch app/generated/__init__.py 