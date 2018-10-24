import json
import math
import time
from datetime import datetime, timedelta, timezone

import RPi.GPIO as GPIO
import dateutil.parser
import pika

PumpPin = 23
PumpSpeed = 2.3


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PumpPin, GPIO.OUT)
    GPIO.output(PumpPin, GPIO.HIGH)


def destroy():
    GPIO.output(PumpPin, GPIO.LOW)
    GPIO.cleanup()


def water(amount):
    time_to_water = math.ceil(amount / PumpSpeed)
    GPIO.output(PumpPin, GPIO.LOW)
    time.sleep(time_to_water)
    GPIO.output(PumpPin, GPIO.HIGH)


def start():
    def callback(ch, method, properties, body):
        print(" [x] Received command %r" % body)
        message = json.loads(body.decode('utf-8'))
        amount = float(message['amount'])
        ttl = int(message['ttl'])
        request_date = dateutil.parser.parse((message['creation_date'])).replace(tzinfo=timezone.utc)
        if request_date + timedelta(seconds=ttl) >= datetime.utcnow().replace(tzinfo=timezone.utc):
            water(amount)
        else:
            print("Message's ttl expired - message will be skiped")

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='water_requests')
    channel.basic_consume(callback, queue='water_requests', no_ack=True)
    print('Start consuming')
    channel.start_consuming()


if __name__ == '__main__':
    print("starting")
    try:
        setup()
        start()
    finally:
        destroy()
