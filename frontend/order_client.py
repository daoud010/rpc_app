import order_pb2 as message
import order_pb2_grpc as service
import grpc


class OrderClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = 50051

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.port))
        self.stub = service.OrderStub(self.channel)

    def AddOrder(self, user_id, order_description, payment_type, payment_card_or_cash_details
                 , order_amount):
        order_info = message.OrderRequest(order_description=order_description, payment_type=payment_type,
                                          payment_card_or_cash_details=payment_card_or_cash_details, order_amount=
                                          order_amount, user_id=user_id)
        return self.stub.AddOrder(order_info)

    def EditOrder(self, order_description, payment_type, payment_card_or_cash_details, order_amount, user_id, order_id):
        order_info = message.OrderRequest_edit(order_description=order_description, payment_type=payment_type,
                                               payment_card_or_cash_details=payment_card_or_cash_details,
                                               order_amount=order_amount, user_id=user_id, order_id=order_id)
        return self.stub.EditOrder(order_info)

    def CancelOrder(self, user_id, order_id):
        order_info = message.OrderRequest_cancel(user_id=user_id, order_id=order_id)
        return self.stub.CancelOrder(order_info)

    def GetAllOrders(self, user_id):
        order_info = message.OrderRequest_all(user_id=user_id)
        return self.stub.GetAllOrders(order_info)

