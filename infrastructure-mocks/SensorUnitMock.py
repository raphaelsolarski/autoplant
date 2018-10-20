import pika
import time
import datetime
import json


class SensorUnitMock:

    def __init__(self):
        self.pause = 10

    # connect to queue and start sending some random data (or maybe a little configured)
    def start(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', port=5672))
        channel = connection.channel()
        channel.queue_declare(queue='measurements')

        while True:
            message = self.create_measurement_message()
            channel.basic_publish(exchange='',
                                  routing_key='measurements',
                                  body=message)
            print('Send message: {}'.format(message))
            time.sleep(self.pause)

    @staticmethod
    def create_measurement_message():
        measurement_date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        message_dict = {'sensor_unit': 's1', 'type': 'temperature', 'date': measurement_date, 'value': '10'}
        return json.dumps(message_dict)


if __name__ == '__main__':
    SensorUnitMock().start()
