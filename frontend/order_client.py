import order_pb2 as message
import order_pb2_grpc as service
import grpc


class OrderClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = 50051

        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.port)
        self.stub = service.OrderStub(self.channel)
        )
