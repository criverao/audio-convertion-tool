import logging
from concurrent import futures
from google.cloud import pubsub_v1
from  google.oauth2 import service_account

logging.basicConfig(level=logging.INFO)

project_id = "northern-symbol-366812"
subscription_id = "AudioConverter-sub"
key_file = '/home/cesa96_gmail_com/key_store/northern-symbol-366812-a5177107a683.json'

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)
cred = service_account.Credentials.from_service_account_file(filename = key_file) #or just from_service_account_file('./auth.json')
publisher = pubsub_v1.PublisherClient(credentials = cred)


def callback(message):
    logging.info("Received %s", message)
    message.ack()

future = subscriber.subscribe(subscription_path, callback=callback)

with subscriber:
    try:
        future.result(timeout=5)
    except futures.TimeoutError:
        future.cancel()  # Trigger the shutdown.
        future.result()  # Block until the shutdown is complete.