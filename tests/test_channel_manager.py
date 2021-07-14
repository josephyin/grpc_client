from grpc_client.channel_manager import ChannelDict


class TestChannelDict:
    def test_compare(self):
        """Channel dict should compared by `ref_count` value"""
        channel1 = ChannelDict(ref_count=1)
        channel2 = ChannelDict(ref_count=2)
        assert channel1 < channel2

    def test_ref(self):
        channel = ChannelDict()
        assert channel.ref == 0

        channel.incr()
        assert channel.ref == 1

        channel.decr()
        channel.decr()
        assert channel.ref == -1
