# Python GRPC Client

A simple GRPC client to easy use.

## Requirements
```
grpcio
protobuf
```

## How to use

### BaseClient

```python
from grpc_client.base_client import BaseClient

def CallbackFunction(response):
    return response

client = BaseClient(
    host='Host',
    port='Port',
    stub_class=GrpcStubClass,
).execute(
    call_func='stub_function_name',
    data={'request': GrpcRequestFunction},
    response_callback=CallbackFunction
)
```

### ChannelClient

`ChannelClient` Reuse channels using channel pools.

```python
import greeter_pb2 as pb2
import greeter_pb2_grpc as pb2_grpc
from grpc_client import ChannelClient, ChannelManager

# Generic using
channel_manager = ChannelManager(address='127.0.0.1:50051', options=options)
response = ChannelClient(
    channel=channel_manager.instance,
    stub_class=pb2_grpc.GreeterStub,
).execute(
    call_func='SayHello',
    data={'request': pb2.HelloRequest(name='Jerry')},
)
# Make sure release finally
channel_manager.release()


# Separate stub and RPC call
channel_manager = ChannelManager(address='127.0.0.1:50051', options=options)
stub = ChannelClient(
    channel=channel_manager.instance,
    stub_class=pb2_grpc.GreeterStub,
)

stub.execute(
    call_func='SayHello',
    data={'request': pb2.HelloRequest(name='Jerry')},
)
stub.execute(
    call_func='SayHi',
    data={'request': pb2.HelloRequest(name='Jerry')},
)
channel_manager.release()


# Context using
with ChannelManager(address='127.0.0.1:50051', options=options) as channel_manager:
    response = ChannelClient(
        channel=channel_manager.instance,
        stub_class=pb2_grpc.GreeterStub,
    ).execute(
        call_func='SayHello',
        data={'request': pb2.HelloRequest(name='Jerry')},
    )
```
