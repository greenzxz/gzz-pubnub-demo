import requests
import time
import threading

from pubnub import Pubnub

default_publish_key = "demo"
default_subscribe_key = "demo"

default_channel = "gzz_private_channel"


class Pubnub_Conn():
    """
    Class which encapsulates handling of a pubnub object.  For now, it assumes the connection is generated elsewhere
    and only handles acccessing a particular channel.
    """

    def __init__(self, pubnub, channel):
        self.pubnub = pubnub
        self.channel = channel
        self.subscribed = threading.Event()

        self.pubnub.subscribe(channels=self.channel, callback=self.incoming_message, error=self.error_cb,
                              connect=self.connect_cb, reconnect=self.reconnect_cb, disconnect=self.disconnect_cb)

    def incoming_message(self, message, channel):
        print(message)

    def error_cb(self, message):
        print("\tERROR : " + str(message))

    def connect_cb(self, message):
        self.subscribed.set()

    def reconnect_cb(self, message):
        self.subscribed.set()
        print("\tRECONNECTED")

    def disconnect_cb(self, message):
        self.subscribed.clear()
        print("\tDISCONNECTED")

    def send_cb(self, message):
        pass

    def discontinue(self):
        self.pubnub.unsubscribe(channel=self.channel)

    def publish(self, message):
        self.pubnub.publish(channel=self.channel, message=message, callback=self.send_cb, error=self.error_cb)

    def wait_until_ready(self):
        self.subscribed.wait()

    def print_status(self):
        print("\nCurrently connected to channel '%s'" % self.channel)


def main_loop(pubnub_conn):
    """
    Takes a PubNub connection and loops a basic chat program by taking all inputs and pushing them as messages to the
    connection directly.
    :param pubnub_conn: Established connection object
    :return: N/A
    """
    pubnub_conn.wait_until_ready()
    pubnub_conn.print_status()

    print "Input messages at the prompt.  Type 'exit()' to quit.\n"

    while(True):
        msg = raw_input("> ")
        if msg == "exit()":
            break
        pubnub_conn.publish(msg)
        time.sleep(1)


if (__name__ == "__main__"):
    pubnub = Pubnub(publish_key=default_publish_key, subscribe_key=default_subscribe_key, ssl_on=False)

    conn = Pubnub_Conn(pubnub, default_channel)

    main_loop(conn)
    conn.discontinue()
