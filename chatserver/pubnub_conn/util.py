"""
Module holding some utility functions for pubnub.  Specifically, get next message.
"""

import threading

class PubNubWrapper():
    message = ""
    channel = ""

    def __init__(self, conn):
        self.conn = conn
        self.message_received = threading.Event()
        self.subscribe_registered = threading.Event()

    def _message_callback(self, message, channel):
        self.message = message
        self.channel = channel
        self.message_received.set()

    def _connect_callback(self, message):
        self.subscribe_registered.set()

    def wait_for_subscribe(self, channel):
        """
        Subscribe to the provided channel but wait for the connection callback before returning.
        :param channel: name of some channel
        :return:
        """
        assert(not self.subscribe_registered.is_set())

        self.conn.subscribe(
            channels=channel,
            callback=self._message_callback,
            connect=self._connect_callback,
        )
        self.subscribe_registered.wait()
        self.subscribe_registered.clear()
        return

    def get_previous_message(self):
        if self.message_received.is_set():
            return self.message, self.channel
        else:
            return self.wait_for_next_message()

    def wait_for_next_message(self):
        """
        Wait for the next message on this channel by doing the following:
            1. Wait for message callback (set by message received event)
        :return: the next message sent on this channel
        """

        self.message_received.clear()
        self.message_received.wait()

        tmp_message = self.message
        tmp_channel = self.channel

        self.message = ""
        self.channel = ""
        return tmp_message, tmp_channel

    def sub_and_wait_for_next_message(self, channel):
        self.wait_for_subscribe(channel)
        self.wait_for_next_message(channel)

    def publish_message(self, channel, message):
        self.conn.publish(
            channel=channel,
            message=message,
        )

    def terminate(self, channel):
        self.conn.unsubscribe(channel=channel)