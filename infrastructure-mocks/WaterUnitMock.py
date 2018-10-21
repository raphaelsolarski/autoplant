import pika


class WaterUnitSensor:
    def start(self):
        def callback(ch, method, properties, body):
            print(" [x] Received command %r" % body)

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='water_requests')
        channel.basic_consume(callback,
                              queue='water_requests',
                              no_ack=True)
        print('Start consuming')
        channel.start_consuming()


if __name__ == '__main__':
    WaterUnitSensor().start()
