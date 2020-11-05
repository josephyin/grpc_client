# Python GRPC Client

A simple GRPC client to easy use.

## Requirements:
```
grpcio
protobuf
```

## How to use:

```
from grpc_client.bbase_client import BaseClient

def CallbackFunction(response):
    return response

client = BaseClient(
    host='Host',
    port='Port',
    stub_class=GrpcStubClass,
    call_func='stub_function_name',
    data={'request': GrpcRequestFunction},
    response_callback=CallbackFunction
).execute()
```
