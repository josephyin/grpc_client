import time

import greeter_pb2 as pb2
import greeter_pb2_grpc as pb2_grpc
from bench import bench
from grpc_client import ChannelManager, ChannelClient

options = [
    ('grpc.keepalive_time_ms', 7200000),
]


def say_hello_generic_way(index):
    channel_manager = ChannelManager(address='127.0.0.1:50051',
                                     options=options)

    response = ChannelClient(
        channel=channel_manager.instance,
        stub_class=pb2_grpc.GreeterStub,
    ).execute(
        call_func='SayHello',
        data={'request': pb2.HelloRequest(name='Jerry')},
    )
    print(response)

    channel_manager.release()


def say_hello_context_way(index):
    with ChannelManager(address='127.0.0.1:50051',
                        options=options) as channel_manager:

        for i in range(1):
            response = ChannelClient(
                channel=channel_manager.instance,
                stub_class=pb2_grpc.GreeterStub,
            ).execute(
                call_func='SayHello',
                data={'request': pb2.HelloRequest(name='Jerry' * 100000)},
            )
            # print(response)


def main():
    count = 1024
    func = say_hello_generic_way
    bench(func, count=count)


if __name__ == "__main__":
    main()
