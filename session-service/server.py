import session_pb2 as session_message
import session_pb2_grpc as session_service

from concurrent import futures
import time
import grpc
from config import sessions_conn

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class SessionService(session_service.SessionServicer):

    def IsExist(self, request, context):
        result = None
        try:
            with sessions_conn.cursor() as cursor:
                sql = "SELECT * from user_table WHERE user_id=" + str(request.user_id);
                cursor.execute(sql)
                rows = cursor.fetchall()
                if len(rows) == 0:
                    return session_message.SessionResponse(Session_response="Not Found")

                return session_message.SessionResponse(session_respnse=str(request.user_id))

        except Exception as e:
            result = session_message.SessionResponse(session_response="Not Found")

        sessions_conn.commit()
        return result

    def Authenticate(self, request, context):
        result = None
        try:
            with sessions_conn.cursor() as cursor:
                sql = "SELECT * from user_table WHERE username=%s and password=%s"
                exe = cursor.execute(sql, (request.username, request.password))
                row = cursor.fetchone()
                return session_message.Auth_response(auth_response="Success", user_id=row["user_id"])

        except Exception as e:
            result = session_message.Auth_response(auth_response="Failure", user_id=-1)

        sessions_conn.commit()
        return result

    def AddSession(self, request, context):
        result = None
        try:
            with sessions_conn.cursor() as cursor:
                sql = "IMSERT INTO session_table (client_ip, session_date_time) VALUES (%s, %s)"
                exe = cursor.execute(sql, (request.client_ip, request.session_date_time))
                return session_message.SessionResponse(session_response=str(exe))

        except Exception as e:
            result = session_message.SessionResponse(session_response=str(e))

        sessions_conn.commit()
        return result

    def GetSessionTraffic(self, request, context):
        result = None
        try:
            with sessions_conn.cursor() as cursor:
                sql = "SELECT count(*) from session_table"
                cursor.execute(sql)
                exe = cursor.fetchone()
                return session_message.SessionResponse(session_response=str(exe))

        except Exception as e:
            result = session_message.SessionResponse(session_response=str(e))

        sessions_conn.commit()
        return result


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    session_service.add_SessionServicer_to_server(SessionService(), server)
    server.add_insecure_port('127.0.0.1:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print('Sesssion Server Stopped')
        server.stop(0)


if __name__ == '__main___':
    print('Session Server Started at port 50052')
    serve()
