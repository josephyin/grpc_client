"""
Channel factory method

Return a channel from channel pool, Internal adjustment in pool size.
MAX_CONCURRENT_PER_CHANNEL is fixed to 64.

There are two concepts:
`logic channel connection`, `physical channel connection`.

logic_count = physical_count *  MAX_CONCURRENT_PER_CHANNEL
"""
import threading
from queue import PriorityQueue

import grpc

MIN_POOL_SIZE = 4

MAX_CONCURRENT_PER_CHANNEL = 64


class ChannelDict(dict):
    def __eq__(self, other):
        return self.ref == other.ref

    def __gt__(self, other):
        return self.ref > other.ref

    @property
    def ref(self):
        return self.get('ref_count', 0)

    def incr(self):
        self.update(ref_count=self.ref + 1)

    def decr(self):
        self.update(ref_count=self.ref - 1)


class ChannelPool:
    """Channel pool implementation priority queue"""
    def __init__(self):
        self._channels = PriorityQueue()
        self._pool_size = 0
        self._lock = threading.Lock()

    def get(self, target, options=None):
        """Get a logic channel connection, or create a new channel

        Supplementary channels will increase when complicated with up to 64
        or when there are no channels
        """
        with self._lock:
            while True:
                # print('self._channels', self._channels.qsize())
                if self._channels.empty():
                    self._append(target, options=options)

                channel = self._channels.get()

                # Reached max concurrent
                if channel.ref == MAX_CONCURRENT_PER_CHANNEL:
                    self._append(target, options=options)

                if channel.ref == -1:
                    continue

                channel.incr()
                self._channels.put(channel)

                return channel

    def close(self, channel):
        """Close a logic channel connection"""
        with self._lock:
            channel.decr()
            if channel.ref == 0 and self._pool_size > MIN_POOL_SIZE:
                channel.decr()
                self._pool_size -= 1

    def _append(self, target, options):
        channel = ChannelDict(
            instance=grpc.insecure_channel(target, options=options),
            ref_count=0,
        )
        self._channels.put(channel)
        self._pool_size += 1


_pool = ChannelPool()


class ChannelManager:
    """
    Retrieve a channel from Channel Pool
    """
    def __init__(self, address, options=None):
        self.address = address
        self.options = options
        self._channel = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    @property
    def instance(self):
        if self._channel is None:
            self._channel = _pool.get(self.address, self.options)
        return self._channel.get('instance')

    def release(self):
        """Release logic connection of channel"""
        if self._channel:
            _pool.close(self._channel)
