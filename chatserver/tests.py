import random

from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.core.urlresolvers import reverse

# Create your tests here.
from .pubnub_conn import myPubnubConn
from .pubnub_conn.util import PubNubWrapper
from pubnub import Pubnub


def _util_add_salt(text):
    return text + str(random.randrange(100))

class PubNubConnTests(TestCase):

    def test_pubnub_interface(self):
        """
        Assert the Pubnub SDK API fundamentally works, and the provided keys are all acceptable.
        """
        myTestChannel = _util_add_salt("gzz_test_pubnub_api")
        myTestMessage = _util_add_salt("pubnub_api_still_functional")
        referenceConn = Pubnub(
            publish_key=myPubnubConn.publish_key,
            subscribe_key=myPubnubConn.subscribe_key,
            ssl_on=True,
        )
        wrapper = PubNubWrapper(referenceConn)

        wrapper.wait_for_subscribe(myTestChannel)
        wrapper.publish_message(myTestChannel, myTestMessage)

        received_msg, received_channel = wrapper.get_previous_message()

        wrapper.terminate(myTestChannel)
        self.assertEquals(myTestMessage, received_msg)
        self.assertEquals(myTestChannel, received_channel)



    def test_conn_can_publish(self):
        """
        Assert that the connection's publish command correctly publishes some message
        """
        myTestChannel = _util_add_salt("gzz_test_conn_can_publish")
        myTestMessage = _util_add_salt("myConn can publish")

        sendConn = myPubnubConn.MyPubnubConn(channel=myTestChannel)
        referenceConn = Pubnub(
            publish_key=myPubnubConn.publish_key,
            subscribe_key=myPubnubConn.subscribe_key,
            ssl_on=True,
            )

        referenceWrapper = PubNubWrapper(referenceConn)
        referenceWrapper.wait_for_subscribe(myTestChannel)

        sendConn.publish(myTestMessage)

        received_msg, received_channel = referenceWrapper.get_previous_message()

        referenceWrapper.terminate(myTestChannel)

        self.assertEquals(myTestMessage, received_msg)
        self.assertEquals(myTestChannel, received_channel)

class ViewTests(TestCase):

    def test_getting_keys_with_good_user(self):
        """
        Assert that attempting to get the subscribe key with an authorized user succeeds.
        :return:
        """
        response = self.client.post(reverse("chatserver:getkeys"), {'username': 'valid', 'password':'goodpasswd'})
        self.assertContains(response, "subscribe_key", 1)
        self.assertContains(response, "channel", 1)
        self.assertNotContains(response, "publish_key")

    def test_getting_keys_with_bad_user(self):
        """
        Assert that attempting to get the subscribe key with an unauthorized user fails.
        :return:
        """
        response = self.client.post(reverse("chatserver:getkeys"), {'username': 'not valid', 'password':'badpasswd'})
        self.assertNotContains(response, "subscribe_key")
        self.assertNotContains(response, "channel")
        self.assertNotContains(response, "publish_key")


    def test_publish_redirects(self):
        """
        Asserts that sending a message using the API redirects to the right outcome
        :return:
        """
        response = self.client.post(reverse("chatserver:send"), {'user': "irrelevant", "text": "irrelevant"})
        self.assertRedirects(response, reverse("chatserver:sent"))


    def test_publish_succeeds_with_good_message(self):
        """
        Asserts that the publish API can send a valid input
        :return:
        """
        myTestChannel = _util_add_salt("gzz_test_publish_good_message")
        myTestMessage = {
            'user': 'test_user',
            'text': _util_add_salt("publishing a good message"),
            'channel': myTestChannel,
        }

        referenceConn = Pubnub(
            publish_key=myPubnubConn.publish_key,
            subscribe_key=myPubnubConn.subscribe_key,
            ssl_on=True,
        )
        wrapper = PubNubWrapper(referenceConn)

        wrapper.wait_for_subscribe(myTestChannel)

        response = self.client.post(reverse("chatserver:send"), myTestMessage)

        received_msg, received_channel = wrapper.get_previous_message()

        wrapper.terminate(myTestChannel)
        self.assertEquals(received_msg['text'], myTestMessage['text'])
        self.assertEquals(myTestChannel, received_channel)



    def test_publish_works_with_bad_message(self):
        """
        Technically, we should test this with every variant of possible bad message ...
        :return:
        """
        myTestChannel = _util_add_salt("gzz_test_publish_bad_message")
        myExpectedChannel = myPubnubConn.default_channel

        myTestMessage = {
            'user': 'test_user',
            'text': _util_add_salt("publishing a good message"),
        }

        referenceConn = Pubnub(
            publish_key=myPubnubConn.publish_key,
            subscribe_key=myPubnubConn.subscribe_key,
            ssl_on=True,
        )
        wrapper = PubNubWrapper(referenceConn)

        wrapper.wait_for_subscribe(myTestChannel)
        wrapper.wait_for_subscribe(myExpectedChannel)

        response = self.client.post(reverse("chatserver:send"), myTestMessage)

        received_msg, received_channel = wrapper.get_previous_message()

        wrapper.terminate(myTestChannel)
        wrapper.terminate(myExpectedChannel)

        self.assertEquals("Did not receive message from user.", received_msg['text'])