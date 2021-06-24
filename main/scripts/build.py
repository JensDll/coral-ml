import os

os.system("python -m grpc_tools.protoc -I protos --python_out=build --grpc_python_out=build protos/stream.proto")
