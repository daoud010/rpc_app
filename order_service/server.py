import session_pb2 as order_message
import order_pb2_grpc as order_service

from session_client import SessionClient
from payment_client import PaymentClient

from concurrent import futures
import time
import grpc
from config import orders_conn

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
session_instance = SessionClient()
payment_instance = PaymentClient()


class OrderService(order_service.OrderServicer):

    def To_JSON(self, cursor):
        return [dict((cursor.description[label][0], value) for label, value in enumerate(row))
                for row in cursor.fetchall()]

    def AddOrder(self, request, context):
        result = None
        try:
            status = session_instance.IsExist(request.user_id)
            if status is None or status.session_response == "Not Found" or status.session_response == "0":
                return order_message.OrderResponse(order_response=str("User not found"))

            try:
                with orders_conn.cursor() as cursor:
                    sql = "INSERT INTO order_table (order_details, user_id) VALUES (%s, " + str(request.user_id) + ")"
                    exe = cursor.execute(sql, request.order_description)
                    sql = "SELECT * FROM order_table WHERE user_id = " + str(request.user_id) + " ORDER BY order_id " \
                                                                                                "DESC LIMIT 1"
                    exe = cursor.execute(sql)

                    row = cursor.fetchone()

                    order_id = row["order_id"]

                    payment_type = request.payment_type
                    payment_card_or_cash_details = request.payment_card_or_cash_details
                    order_amount = request.order_amount

                    status_payment = payment_instance.AddPayment(payment_type, payment_card_or_cash_details,
                                                                 order_amount,
                                                                 order_id)
                    return order_message.OrderResponse(order_response="Success")
            except Exception as e:
                result = order_message.OrderResponse(order_response="Failure")

        except:
            result = order_message.OrderResponse(order_response="Cant connect with Database Session")

        orders_conn.commit()
        return result

    def EditOrder(self, request, context):
        result = None
        try:
            status = session_instance.IsExist(request.user_id)
            if status is None or status.session_response == "Not Found" or status.session_response == "0":
                return order_message.OrderResponse(order_response=str("User not found"))

            try:
                with orders_conn.cursor() as cursor:
                    sql = "UPDATE order_table set order_details=%s WHERE user_id=" + str(request.user_id)
                    exe = cursor.execute(sql, request.order_description)
                    res = payment_instance.UpdatePayment(request.payment_type, request.payment_card_or_cash_details,
                                                         request.order_amount, request.order_id)

                    if res is None:
                        return order_message.OrderResponse(order_response="Error: can't update the record in "
                                                                          "Payments table ")
                    else:
                        return order_message.OrderResponse(order_response=str(exe))
            except Exception as e:
                result = order_message.OrderResponse(order_response=str(e))

        except:
            result = order_message.OrderResponse(order_response="Cant connect with Database Session")

        orders_conn.commit()
        return result

    def CancelOrder(self, request, context):
        result = None
        try:
            status = session_instance.IsExist(request.user_id)
            if status is None or status.session_response == "Not Found" or status.session_response == "0":
                return order_message.OrderResponse(order_response=str("User not found"))
            try:

                with orders_conn.cursor() as cursor:
                    sql = "DELETE FROM order_table WHERE order_id=" + str(request.order_id) + "  AND user_id=" \
                          + str(request.user_id) + ""
                    exe = cursor.execute(sql)

                    res = payment_instance.DeletePayment(request.order_id)

                    if res is None:
                        return order_message.OrderResponse(order_response="Error: Can't Delete the record in Payments "
                                                                          "table")
                    else:
                        return order_message.OrderResponse(order_response=str(exe))
            except Exception as e:
                result = order_message.OrderResponse(order_response=str(e))
        except:
            result = order_message.OrderResponse(order_response="Cant connect with Database Session")

        orders_conn.commit()
        return result

    def GetAllOrders(self, request, context):
        result = None
        try:
            status = session_instance.IsExist(request.user_id)
            if status is None or status.session_response == "Not Found" or status.session_response == "0":
                return order_message.OrderResponse(order_response=str("User not found"))
            try:
                with orders_conn.cursor() as cursor:
                    sql = "SELECT * from order_table WHERE user_id" + str(request.user_id)
                    exe = cursor.execute(sql)

                    rows = cursor.fetchall()
                    all_records = order_message.OrderResponse_all()

                    for row in rows:
                        payment_record = payment_instance.GetPaymentById(row["order_id"]).payment_response
                        payment_type = payment_record.payment_type
                        payment_card_or_cash_details = payment_record.payment_card_or_cash_details
                        order_amount = payment_record.order_amount
                        all_records.order_response.append(order_message.OrderResponse_get
                                                          (order_description=row["order_details"],
                                                           payment_type=payment_type,
                                                           payment_card_or_cash_details=payment_card_or_cash_details,
                                                           order_amount=order_amount,
                                                           order_id=row["order_id"]))
                    return all_records
            except Exception as e:
                result = all_records
        except:
            result = None

        orders_conn.commit()
        return result


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_service.add_OrderServicer_to_server(OrderService(), server)
    server.add_insecure_port('127.0.0.1:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print('Order Server Stopped')
        server.stop(0)


if __name__ == '__main__':
    print('Order Server Started at port 50051')
    serve()
