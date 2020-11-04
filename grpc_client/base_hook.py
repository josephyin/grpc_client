"""GRPC Hook"""
import logging
from typing import Callable, Generator, Optional

import grpc


class BaseHook:
    """
    General interaction with gRPC servers.
    :param host: The host to use when connection.
    :type host: str
    :param port: The port to use when connection.
    :type port: str
    """

    def __init__(
            self,
            host: str,
            port: str
    ) -> None:
        self.host = host
        self.port = port
        self.log = logging.getLogger(
            self.__class__.__module__ + '.' + self.__class__.__name__
        )

    def get_conn(self) -> grpc.Channel:
        base_url = self.host

        if self.port:
            base_url = base_url + ":" + str(self.port)
        channel = grpc.insecure_channel(base_url)
        return channel

    def run(self,
            stub_class: Callable,
            call_func: str,
            streaming: bool = False,
            data: Optional[dict] = None) -> Generator:
        """Call gRPC function and yield response to caller"""
        if data is None:
            data = {}
        with self.get_conn() as channel:
            stub = stub_class(channel)
            try:
                rpc_func = getattr(stub, call_func)
                response = rpc_func(**data)
                if not streaming:
                    yield response
                else:
                    yield from response
            except grpc.RpcError as ex:
                self.log.exception(
                    "Error occurred when calling the grpc service: %s, method: %s \
                    status code: %s, error details: %s",
                    stub.__class__.__name__,
                    call_func,
                    ex.code(),  # pylint: disable=no-member
                    ex.details(),  # pylint: disable=no-member
                )
                raise ex
