import time
import json
import random
from datetime import datetime
from data import generate_message
from kafka import KafkaProducer


# Mensajes son serializados como JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

if __name__ == '__main__':
    while True:
        # Generar el mensaje
        dummy_message = generate_message()

        # Enviar el mesaje al topico 'mensajes'
        print(f'Producing message @ {datetime.now()} | Message = {str(dummy_message)}')
        producer.send('messages', dummy_message)

        # Esperar tiempo aleatorio de segundos
        time_to_sleep = random.randint(1, 11)
        time.sleep(time_to_sleep)
