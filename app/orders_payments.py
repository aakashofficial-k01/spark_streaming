from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime, timedelta
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['kafka:29092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

order_ids = []
# topics = ['orders', 'payments']
# for topic_name in topics:
#     try:
#         admin_client = KafkaAdminClient(
#             bootstrap_servers='kafka:29092'
#         )
#         topic = NewTopic(name=topic_name,
#                          num_partitions=1,
#                          replication_factor=1)
#         admin_client.create_topics([topic])
#         print(f"Topic {topic_name} created")
#
#     except Exception as e:
#         print(f"Topic creation error: {e}")
while True:
    try:
        # Generate order
        order_id = str(random.randint(1000, 9999))
        order_ids.append(order_id)

        order = {
            'order_id': order_id,
            'amount': random.randint(100, 1000),
            'timestamp': (datetime.now() - timedelta(minutes=random.randint(0, 2))).isoformat()
        }

        producer.send('orders', order)
        print(f"Order: {order}")

        # Generate payment (70% probability)
        if order_ids and random.random() < 0.7:
            payment = {
                'order_id': random.choice(order_ids),
                'payment_amount': random.randint(100, 1000),
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(0, 1))).isoformat()
            }
            producer.send('payments', payment)
            print(f"Payment: {payment}")

        time.sleep(3)

    except KeyboardInterrupt:
        producer.close()
        break