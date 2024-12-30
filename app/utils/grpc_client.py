import grpc
from app.generated import user_pb2, user_pb2_grpc
from contextlib import contextmanager

class SecureGrpcClient:
    def __init__(self, target='localhost:50051', cert_path='certs/server.crt'):
        self.target = target
        self.cert_path = cert_path
        self._channel = None
        self._stub = None

    def _create_channel(self):
        with open(self.cert_path, 'rb') as f:
            root_certificates = f.read()
        credentials = grpc.ssl_channel_credentials(root_certificates)
        return grpc.secure_channel(self.target, credentials)

    @property
    def stub(self):
        if self._stub is None:
            self._channel = self._create_channel()
            self._stub = user_pb2_grpc.UserServiceStub(self._channel)
        return self._stub

    def close(self):
        if self._channel is not None:
            self._channel.close()
            self._channel = None
            self._stub = None

    @contextmanager
    def channel_scope(self):
        try:
            yield self.stub
        finally:
            self.close()

# 使用示例
client = SecureGrpcClient()
with client.channel_scope() as stub:
    response = stub.GetUser(user_pb2.GetUserRequest(user_id=1)) 