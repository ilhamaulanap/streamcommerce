import requests
import json
import time
from confluent_kafka import SerializingProducer
from datetime import datetime

api_key = '55df03be-e10b-42ac-ba79-d481b2739f9d'
url = f'http://api.airvisual.com/v2/countries?key={api_key}'


def fetch_weather_data(url):
    try:
        fetch_data = requests.get(url)
        fetch_data.raise_for_status()
        weather_data = fetch_data.json()
        return weather_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred' : {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error Occurred: {conn_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"an Error occurred: {req_err}")

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f"Message delivered to {msg.topic} [{msg.partition()}]")


def main(url):
    topic = 'test_data'
    
    producer = SerializingProducer ({'bootstrap.servers': 'localhost:9092'})



    while True:
        try:
            weather_data = fetch_weather_data(url)

            print(weather_data)

            producer.produce(topic,
                             value=json.dumps(weather_data),
                             on_delivery=delivery_report
                             )
            producer.poll(0)
            time.sleep(5)
        except BufferError:
            print("buffer full! waiting....")
            time.sleep(1)
        except Exception as e:
            print(e)
