import pika
import time
import datetime
import json
from random import randint, random

class SensorUnitMock:

    def __init__(self):
        self.pause = 10
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', port=5672))
        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(queue='measurements')

    # connect to queue and start sending some random data (or maybe a little configured)
    def start(self):
        while True:
            self.send_measurement_message(1, 'temperature', randint(0, 20))
            self.send_measurement_message(1, 'humidity', random())
            time.sleep(self.pause)

    def send_measurement_message(self, sensor_unit_id, measurement_type, value):
        measurement_date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        message_dict = {'sensor_unit': sensor_unit_id, 'type': measurement_type, 'date': measurement_date, 'value': value}
        message = json.dumps(message_dict)
        self.__channel.basic_publish(exchange='',
                                     routing_key='measurements',
                                     body=message)
        print('Send message: {}'.format(message))


if __name__ == '__main__':
    SensorUnitMock().start()
