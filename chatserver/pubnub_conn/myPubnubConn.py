"""
Class to contain some pubnub connection functionality
"""

import threading
from pubnub import Pubnub

publish_key = "pub-c-bc724c66-7439-42cc-ac8a-c1277dd51544"
subscribe_key = "sub-c-80b8bd2c-7c24-11e5-8495-02ee2ddab7fe"

cipher_key = "XJKBQ0KF592YNGZA160D"

default_channel = "gzz_chat_lobby"

class MyPubnubConn():

    def __init__(self, channel):
        self.conn = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key, ssl_on=True,
                           # cipherkey randomly generated for purposes of PoC, but it is too short and needs to be
                           #   securely stored.
                           # cipher_key=cipher_key
                           )
        self.channel = channel
        self.subscribed = threading.Event()

        # server doesn't need to subscribe, only publish
        #self.conn.subscribe(channels=self.channel, callback=self.incoming_message, error=self.error_cb,
        #                     connect=self.connect_cb, reconnect=self.reconnect_cb, disconnect=self.disconnect_cb)

    def incoming_message(self, message, channel):
        pass
        #print(message)

    def error_cb(self, message):
        pass
        #print("\tERROR : " + str(message))

    def connect_cb(self, message):
        self.subscribed.set()

    def reconnect_cb(self, message):
        self.subscribed.set()
        #print("\tRECONNECTED")

    def disconnect_cb(self, message):
        self.subscribed.clear()
        #print("\tDISCONNECTED")

    def send_cb(self, message):
        pass

    def discontinue(self):
        self.conn.unsubscribe(channel=self.channel)

    def publish(self, message):
        self.conn.publish(channel=self.channel, message=message, callback=self.send_cb, error=self.error_cb)

    def wait_until_ready(self):
        self.subscribed.wait()

    def print_status(self):
        print("\nCurrently connected to channel '%s'" % self.channel)