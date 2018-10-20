import pika


class WaterUnitSensor:
    def start(self):
        def callback(ch, method, properties, body):
            print(" [x] Received command %r" % body)

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='measurements')
        channel.basic_consume(callback,
                              queue='measurements',
                              no_ack=True)
        print('Start consuming')
        channel.start_consuming()


if __name__ == '__main__':
    WaterUnitSensor().start()
