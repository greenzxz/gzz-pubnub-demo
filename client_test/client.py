import time
import threading
import requests

from pubnub import Pubnub

local = False

if local:
    DEFAULT_URL_BASE="http://%s:%d"
    DEFAULT_HOST="localhost"
    DEFAULT_PORT=5000
else:
    DEFAULT_URL_BASE="https://%s:%d"
    DEFAULT_HOST="gzz-pubnub-demo.herokuapp.com"
    DEFAULT_PORT=443

DEFAULT_APP_BASE="chat"

LOGIN_URI="login"
SEND_URI="send_msg"

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
        print("%s: %s" % (channel, message))

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

def get_subscription_key():
    uri = DEFAULT_URL_BASE % (DEFAULT_HOST, DEFAULT_PORT) + "/" + DEFAULT_APP_BASE + "/" + LOGIN_URI
    resp = requests.post(uri, {'username': "anonymous", "password": "bad_pw"})

    print uri
    print resp
    server_data = resp.json()

    return (server_data['sub_key'], server_data['channel'])

def main_loop(send_uri):
    while(True):
        msg = raw_input("> ")
        if msg == "exit()":
            print "Goodbye!"
            break

        if len(msg) > 0:
            resp = requests.post(send_uri, {"text": msg, "source": "anonymous"})
            time.sleep(1)

def default_listener():
    sub_key, channel = get_subscription_key()

    pubnub = Pubnub(publish_key="", subscribe_key=sub_key, ssl_on=False)
    conn = Pubnub_Conn(pubnub, channel)

    conn.wait_until_ready()
    conn.print_status()

    print "Input messages at the prompt.  Type 'exit()' to quit.\n"

    send_uri = DEFAULT_URL_BASE % (DEFAULT_HOST, DEFAULT_PORT) + "/" + DEFAULT_APP_BASE + "/" + SEND_URI
    main_loop(send_uri)

    conn.discontinue()

if (__name__ == "__main__"):
    default_listener()
