cd /usercode/session-service/
python3 -m grpc_tools.protoc --proto_path=../protos/ ../protos/session.proto --python_out =.--grpc_python_out=.
python3 server.py &
cd /usercode/payment-service/
python3 -m grpc_tools.protoc --proto_path=../protos/ ../protos/payment.proto --python_out =. --grpc_python_out=.
python3 server.py &
cd /usercode/order-service
python3 -m grpc_tools.protoc --proto_path=../protos/ ../protos/order.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=../protos/  ../protos/session.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools,oritic --proto_path=../protos/ ../protos/payment.proto --python_out=. --grpc_python_out=.
python3 server.py &
cd /usercode/Frontend
python3 -m grpc_tools.protoc --proto_path=../protos/ ../protos/order.proto --python_out=. --grpc_python_out=.
pyhton3 - m grpc_tools.protoc --proto_path=../protos/ ../protos/session.proto --python_out=. --grpc_python_out=.
export FLASK_APP=client_app.py
echo "Running client on port 8080"
waitress-serve --host=0.0.0.0 --port=8080 --call client_app:create_app

