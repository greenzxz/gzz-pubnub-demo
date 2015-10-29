# Initial Green Zhang's pubnub demo.

This is a simple chat powered by Pubnub.  However, this app assumes that the back-end server will be the main publisher
of messages and removes that right from the clients.  The clients, when typing messages, will send them to the server
first.

This allows more convenient future control over users.  The natural PubNub style would use auth_key and individual clients,
but this doesn't put control over type of messages sent.

Note: Two known issues with the django tests:

1. One written test is expected to fail, because user authentication is not turned on.  This is intended to show how the
tests should look.

2. PubNub seems sometimes slow to close a python connection.  Either wait a decent amount of time, or force kill after the
tests are completed.