"""GRPC Hook"""
import logging
from typing import Callable, Generator, Optional

import grpc

from .base_hook import BaseHook


class ChannelHook(BaseHook):
    """
    General interaction with gRPC servers using Channel Pool.
    """
    def __init__(self, channel) -> None:
        self.channel = channel
        super().__init__(host='', port='')

    def get_conn(self) -> grpc.Channel:
        return self.channel

    def run(self,
            stub_class: Callable,
            call_func: str,
            streaming: bool = False,
            data: Optional[dict] = None) -> Generator:
        """
        Call gRPC function and yield response to caller using Channel client
        """
        if data is None:
            data = {}
        channel = self.get_conn()
        # print('Get channel connection: %r' % channel)
        stub = stub_class(channel)
        yield from self.call_rpc(stub, call_func, streaming, data)
