import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from dotenv import load_dotenv

load_dotenv()

credentials_path = './privatekey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/pubsub-397308/subscriptions/adopisoft-machine-payments-sub'

def record_payment(message):
    print(f'Received payment from machine id: xxxx: {message}')
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=record_payment)

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

