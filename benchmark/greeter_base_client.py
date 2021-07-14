import time

import greeter_pb2 as pb2
import greeter_pb2_grpc as pb2_grpc
from bench import bench
from grpc_client.base_client import BaseClient


def say_hello(index):
    for i in range(1):
        response = BaseClient(
            host='127.0.0.1',
            port='50051',
            stub_class=pb2_grpc.GreeterStub,
        ).execute(
            call_func='SayHello',
            data={'request': pb2.HelloRequest(name='Jerry')},
        )
        # print(response)


def main():
    count = 1024
    func = say_hello
    bench(func, count=count)


if __name__ == "__main__":
    main()
