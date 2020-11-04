import logging
from typing import Callable, Optional, Any

from .base_hook import BaseHook


class BaseClient:
    """
    Calls a gRPC endpoint to execute an action
    :param host: The host to use when connection.
    :type host: str
    :param port: The port to use when connection.
    :type port: str
    :param stub_class: The stub client to use for this gRPC call
    :type stub_class: gRPC stub class generated from proto file
    :param call_func: The client function name to call the gRPC endpoint
    :type call_func: gRPC client function name for the endpoint generated from proto file, str
    :param data: The data to pass to the rpc call
    :type data: A dict with key value pairs as kwargs of the call_func
    :param streaming: A flag to indicate if the call is a streaming call
    :type streaming: boolean
    :param response_callback: The callback function to process the response from gRPC call
    :type response_callback: A python function that process the response from gRPC call,
        takes in response object
    :param log_response: A flag to indicate if we need to log the response
    :type log_response: boolean
    """

    def __init__(
            self,
            *,
            host: str,
            port: str,
            stub_class: Callable,
            call_func: str,
            data: Optional[dict] = None,
            streaming: bool = False,
            response_callback: Optional[Callable] = None,
            log_response: bool = False
    ) -> None:
        self.host = host
        self.port = port
        self.stub_class = stub_class
        self.call_func = call_func
        self.data = data or {}
        self.streaming = streaming
        self.log_response = log_response
        self.response_callback = response_callback
        self.log = logging.getLogger(
            self.__class__.__module__ + '.' + self.__class__.__name__
        )

    def _get_grpc_hook(self) -> BaseHook:
        return BaseHook(
            self.host, self.port
        )

    def execute(self) -> None:
        hook = self._get_grpc_hook()
        self.log.info("Calling gRPC service")

        # grpc hook always yield
        responses = hook.run(self.stub_class, self.call_func, streaming=self.streaming, data=self.data)

        for response in responses:
            self._handle_response(response)

    def _handle_response(self, response: Any) -> None:
        if self.log_response:
            self.log.info(repr(response))
        if self.response_callback:
            self.response_callback(response)
