# Efficient Payment Notification Script with 5ms Polling Delay
#
# This script efficiently listens for payment notifications from a PostgreSQL database
# and publishes them to Google Cloud Pub/Sub. It aims to strike a balance between
# resource efficiency and responsiveness. While being less resource-intensive,
# it introduces a 5ms polling delay, which ensures a reasonable interval between
# consecutive database polls.
#
# Requirements:
# - psycopg2: PostgreSQL adapter for Python (pip install psycopg2)
# - google-cloud-pubsub: Google Cloud Pub/Sub client library (pip install google-cloud-pubsub)
#
# Setup:
# - Configure PostgreSQL and Google Cloud Pub/Sub credentials via environment variables.
# - Set up the appropriate topic path for Pub/Sub.
#
# How it works:
# - The script establishes a persistent database connection and listens for notifications.
# - Upon receiving a notification, it extracts relevant payment data and publishes it.
# - A 5ms polling delay between consecutive polls reduces resource usage while maintaining
#   reasonable responsiveness.
#
# Note:
# - This code is optimized for scenarios where the database notifications are not extremely time-sensitive.
# - If precise timing is critical, consider adjusting the polling delay or use v1 instead.
#
# Author: Maynard Magallen
# Date: August 29, 2023
# GitHub: https://github.com/KleKlai/Adopisoft-Payment-pubsub
#
# -- Enjoy efficient payment tracking! --

import os
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import time

load_dotenv()

def connect_to_database():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

def publish_notification(topic_path, machine_id, amount, created_at):
    publisher = pubsub_v1.PublisherClient()
    data = 'Payment Received!'.encode('utf-8')
    publisher.publish(topic_path, data, machine_id=machine_id, amount=amount, created_at=created_at)

def main():
    connection = connect_to_database()
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute("LISTEN payment_notification;")

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    topic_path = 'projects/pubsub-397308/topics/adopisoft-machine-payments'

    while True:
        connection.poll()
        if connection.notifies:
            notify = connection.notifies.pop(0)
            parsed_data = json.loads(notify.payload)
            machine_id = parsed_data.get('machine_id').encode('utf-8')
            amount = str(parsed_data.get('amount')).encode('utf-8')
            created_at = parsed_data.get('created_at').encode('utf-8')
            publish_notification(topic_path, machine_id, amount, created_at)

        else:
            time.sleep(5)  # Wait for 5 seconds before polling again

if __name__ == "__main__":
    main()
