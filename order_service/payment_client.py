import payment_pb2 as message
import payment_pb2_grpc as service
import grpc


class PaymentClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = 50053

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.port))
        self.stub = service.PaymentStub(self.channel)

    def AddPayment(self, payment_type, payment_card_or_cash_details, order_amount, order_id):
        payment_info = message.PaymentRequest(payment_type=payment_type,
                                              payment_card_or_cash_details=payment_card_or_cash_details,
                                              order_id=order_id)
        return self.stub.AddPayment(payment_info)

    def GetPaymentById(self, order_id):
        payment_info = message.PaymentRequest(order_id=order_id)
        return self.stub.GetPaymentById(payment_info)

    def DeletePayment(self, order_id):
        payment_info = message.PaymentRequest_del(order_id=order_id)
        return self.stub.DeletePayment(payment_info)

    def UpdatePayment(self, payment_type, payment_card_or_cash_details, order_amount, order_id):
        payment_info = message.PaymentRequest(payment_type=payment_type,
                                              payment_card_or_cash_details=payment_card_or_cash_details,
                                              order_amount=order_amount,
                                              order_id=order_id)
        return self.stub.UpdatePayment(payment_info)

