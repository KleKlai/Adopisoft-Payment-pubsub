import os
from google.cloud import pubsub_v1
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import select
import json
from dotenv import load_dotenv

load_dotenv()

# Establish Database Connection 
connection = psycopg2.connect(
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    dbname = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
cursor.execute("LISTEN payment_notification;")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/pubsub-397308/topics/adopisoft-machine-payments'

data = 'Payment Received!'.encode('utf-8')

while True:
    if select.select([connection],[],[],5) == ([],[],[]):
        print("Timeout")
    else:
        connection.poll()
        while connection.notifies:
            notify = connection.notifies.pop(0)
            parsed_data = json.loads(notify.payload)
            machine_id = parsed_data.get('machine_id').encode('utf-8')
            amount = str(parsed_data.get('amount'))
            created_at = parsed_data.get('created_at').encode('utf-8')
            publisher.publish(topic_path, data, machine_id=machine_id, amount=amount, created_at=created_at)