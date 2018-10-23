import json
import os

import django
import pika


def start():
    def callback(ch, method, properties, body):
        try:
            print('Received message: {}'.format(body))
            message = json.loads(body, encoding="utf8")
            sensor_unit_id = message['sensor_unit']
            if SensorUnit.objects.filter(id=sensor_unit_id).exists():
                sensor_unit = SensorUnit.objects.get(id=sensor_unit_id)
                obj = Measurement.objects.create(sensor_unit=sensor_unit,
                                                 type=message['type'],
                                                 date=message['date'],
                                                 value=message['value'])
                obj.save()
            else:
                print('Receiving message from not configured sensor unit - message will be skiped')
        except Exception as e:
            print('Error during processing message: {}'.format(body), e)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='measurements')
    channel.basic_consume(callback,
                          queue='measurements',
                          no_ack=True)
    print('Start consuming')
    channel.start_consuming()


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoplant.settings")
    django.setup()
    from centralunit.models import Measurement, SensorUnit

    start()
