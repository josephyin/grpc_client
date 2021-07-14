import logging
from concurrent import futures

import grpc

import greeter_pb2
import greeter_pb2_grpc


class Greeter(greeter_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return greeter_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    options = [
        ('grpc.keepalive_time_ms', 7200000),
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=256),
                         options=options)
    greeter_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Service greeter started")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
