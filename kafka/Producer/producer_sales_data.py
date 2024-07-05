import json
import random
import time
from faker import Faker
from confluent_kafka import SerializingProducer
from datetime import datetime

fake = Faker()

def generate_sales_transactions():
    user = fake.simple_profile()

    return {
        "transactionId": fake.uuid4(),
        "productId": random.choice(['product1', 'product2', 'product3', 'product4', 'product5', 'product6']),
        "productName": random.choice(['laptop', 'mobile', 'tablet', 'watch', 'headphone', 'speaker']),
        'productCategory': random.choice(['electronic', 'fashion', 'grocery', 'home', 'beauty', 'sports']),
        'productPrice': round(random.uniform(10, 1000), 2),
        'productQuantity': random.randint(1, 10),
        'productBrand': random.choice(['apple', 'samsung', 'oneplus', 'mi', 'boat', 'sony']),
        'currency': random.choice(['USD', 'GBP']),
        'customerId': user['username'],
        'transactionDate': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "paymentMethod": random.choice(['credit_card', 'debit_card', 'online_transfer'])
    }

def generate_customer_feedback():
    user = fake.simple_profile()

    return {
        "feedbackId": fake.uuid4(),
        "customerId": user['username'],
        "productId": random.choice(['product1', 'product2', 'product3', 'product4', 'product5', 'product6']),
        "rating": random.randint(1, 5),
        "comment": fake.text(max_nb_chars=200),
        "feedbackDate": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    }

def generate_product_view():
    return {
        "productId": random.choice(['product1', 'product2', 'product3', 'product4', 'product5', 'product6']),
        "viewCount": random.randint(1, 100),
        "lastViewed": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    }

def generate_website_traffic():
    return {
        "pageUrl": random.choice([
            '/home', 
            '/products', 
            '/cart', 
            '/checkout', 
            '/contact', 
            '/about'
        ]),
        "visitCount": random.randint(1, 1000),
        "lastVisit": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    }

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f"Message delivered to {msg.topic} [{msg.partition()}]")

def main():

    #kafka topics
    transactions_topic = 'financial_transactions'
    feedback_topic = 'customer_feedback'
    views_topic = 'product_views'
    traffic_topic = 'website_traffic'

    producer = SerializingProducer({
        'bootstrap.servers': 'localhost:9092'
    })

    while True:
        try:
            transaction = generate_sales_transactions()
            transaction['totalAmount'] = transaction['productPrice'] * transaction['productQuantity']

            customer_feedback = generate_customer_feedback()

            product_view = generate_product_view()

            website_traffic = generate_website_traffic()

            print(transaction)
            print(customer_feedback)
            print(product_view)
            print(website_traffic)

            # Send transaction data
            producer.produce(transactions_topic,
                             key=transaction['transactionId'],
                             value=json.dumps(transaction),
                             on_delivery=delivery_report
                             )
            producer.poll(0)

            # Send customer feedback data
            producer.produce(feedback_topic,
                             key=customer_feedback['feedbackId'],
                             value=json.dumps(customer_feedback),
                             on_delivery=delivery_report
                             )
            producer.poll(0)

            # Send product view data
            producer.produce(views_topic,
                             key=product_view['productId'],
                             value=json.dumps(product_view),
                             on_delivery=delivery_report
                             )
            producer.poll(0)

            # Send website traffic data
            producer.produce(traffic_topic,
                             key=website_traffic['pageUrl'],
                             value=json.dumps(website_traffic),
                             on_delivery=delivery_report
                             )
            producer.poll(0)

            # Wait for 10 seconds before sending the next set of data
            time.sleep(10)
        except BufferError:
            print("Transaction buffer full! Waiting...")
            time.sleep(1)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
