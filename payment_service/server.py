import payment_pb2_grpc as payment_message
import payment_pb2_grpc as payment_service

from concurrent import futures
import time
import grpc
from config import payments_conn

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class PaymentService(payment_service.PaymentServicer):

    def AddPayment(self, request, context):
        result = None
        try:
            with payments_conn.cursor() as cursor:
                sql = "INSERT INTO payment_table (payment_type, payment_card_or_cash_details, order_amount, order_id) " \
                      "VALUES (%s, %s, " + str(request.order_amount) + ", " + str(request.order_id) + ")"
                exe = cursor.execute(sql, (request.payment_type, request.payment_card_or_cash_details))
                return payment_message.PaymentResponse_message(payment_response=str(exe))

        except Exception as e:
            result = payment_message.PaymentResponse(payment_response=str(e))

        payments_conn.commit()
        return result

    def UpdatePayment(self, request, context):
        result = None
        try:
            with payments_conn.cursor() as cursor:
                sql = "UPDATE payment_table set payment_type=%s, payment_card_or_cash_details=%s, order_amount=" \
                      + str(request.order_amount) + " WHERE order_id=" + str(request.order_id)
                exe = cursor.execute(sql, (request.payment_type, request.payment_card_or_cash_details))
                return payment_message.PaymentResponse_message(payment_response="Success")
        except Exception as e:
            result = payment_message.PaymentResponse_message(payment_response="Failure")

        payments_conn.commit()
        return result

    def GetPaymentById(self, request, context):
        result = None
        try:
            with payments_conn.cursor() as cursor:
                sql = "SELECT * from payment_table where order_id" + str(request.order_id)
                exe = cursor.execute(sql)
                fetch = cursor.fetchone()

                payment_type = fetch["payment_type"]
                payment_card_or_cash_details = fetch["payment_card_or_cash_details"]
                order_amount = fetch["order_amount"]

                record = payment_message.PaymentResponse_show(payment_type=payment_type,
                                                              payment_card_or_cash_details=payment_card_or_cash_details,
                                                              order_amount=order_amount)

                return payment_message.PaymentResponse_message(payment_response=record)

        except Exception as e:
            result = payment_message.PaymentResponse_message(payment_response=str(e))

        payments_conn.commut()
        return result

    def DeletePayment(self, request, context):
        result = None
        try:
            with payments_conn.cursor() as cursor:
                sql = "DELETE from payment_table whrere order_id=" + str(request.order_id) + ""
                exe = cursor.execute(sql)
                return payment_message.PaymentResponse_message(payment_response=str(exe))

        except Exception as e:
            result = payment_message.PaymentResponse_message(payment_response=str(e))

        payments_conn.commit()
        return result


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_service.add_PaymentServicer_to_server(PaymentService(), server)
    server.add_insecure_port('127.0.0.1:50053')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print('Payment Server Stop')
        server.stop(0)

    if __name__ == '__main__':
        print('Payment Server Started at port 50053')
        serve()
