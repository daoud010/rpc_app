import session_pb2 as message
import session_pb2_grpc as service
import grpc


class SessionClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = 50052

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.port))

        self.stub = service.SessionStub(self.channel)

    def Authenticate(self, username, password):
        user_info = message.Auth_user(username= username, password=password)
        return self.stub.Authenticate(user_info)

    def IsExist(self, user_id):
        user_info = message.User(user_id=user_id)
        return self.stub.IsExist(user_info)

    def AddSession(self, client_ip, session_date_time, user_id):
        session_info = message.SessionRequest(client_ip= client_ip, session_date_time=session_date_time,
                                              user_id=user_id)
        return self.stub.AddSession(session_info)

    def GetSessionTraffic(self):
        session_info = message.SessionRequest_No_Params()
        return self.stub.GetSessionTraffic(session_info)

