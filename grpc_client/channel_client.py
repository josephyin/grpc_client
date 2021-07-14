from typing import Callable, Optional, Generator

import grpc

from .base_client import BaseClient
from .channel_hook import ChannelHook


class ChannelClient(BaseClient):
    """
    Calls a gRPC endpoint to execute an action using Channel Pool.
    """
    def __init__(self, *, channel, stub_class: Callable) -> None:
        """
        :param channel: gRPC channel
        :param stub_class:
        """

        self.channel = channel
        super().__init__(host='', port='', stub_class=stub_class)

    def _get_grpc_hook(self) -> ChannelHook:
        return ChannelHook(self.channel)
