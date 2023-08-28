# Real-Time Payment Tracking System with Pub/Sub Integration

This repository contains a real-time payment tracking system that utilizes Google Cloud Pub/Sub for efficient communication and updates. The system ensures accurate and instant payment tracking, enhancing financial transparency and efficiency.

## Features

- **Real-Time Updates:** Enjoy instant payment notifications, eliminating delays in payment processing.
- **Secure Database Integration:** Establish a secure connection to a PostgreSQL database for reliable data storage.
- **Google Cloud Pub/Sub Integration:** Leverage Google Cloud Pub/Sub for efficient communication between components.
- **Easy Configuration:** Utilize environment variables for streamlined setup and configuration.

## Installation

1. Install required packages using the following command: pip install -r requirements.txt

2. Set up your environment variables in a `.env` file. You can refer to `.env.example` for the required variables.

3. Ensure your PostgreSQL and Google Cloud Pub/Sub configurations are accurate.

## Usage

1. Run the payment notification producer script:
```bash
python payment_notification_producer.py
```

2. Run the payment subscriber script
```
python payment_subscriber.py
```

## Get Involved
Contribute to our open-source project by submitting pull requests, raising issues, and collaborating with the community. Your contributions help us enhance payment processing for everyone!

Let's simplify payment recording and tracking together. Join us on this journey and make an impact! 🚀
