from setuptools import setup, find_packages

setup(
    name="grpc_fastapi_example",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "grpcio",
        "grpcio-tools",
        "fastapi",
        "uvicorn",
        "requests"
    ],
) 