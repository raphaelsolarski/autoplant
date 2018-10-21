import json
import logging
from datetime import timedelta, date, datetime

import pika
from django.conf import settings
from django.utils import timezone

from centralunit.models import ScheduledWatering, CyclicSchedule

logger = logging.getLogger(__name__)


class Scheduler:

    def __init__(self):
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.WATERING_REQUESTS_BROKER_URL,
            port=settings.WATERING_REQUESTS_BROKER_PORT))
        self.__channel = self.__connection.channel()
        self.__queue_name = settings.WATERING_REQUESTS_BROKER_QUEUE_NAME
        self.__routing_key = settings.WATERING_REQUESTS_BROKER_ROUTING_KEY
        self.__channel.queue_declare(queue=self.__queue_name)

    def check_and_schedule(self):
        cyclic_schedules = CyclicSchedule.objects.filter(active=True)
        for schedule in cyclic_schedules:
            self.__deal_with_single_schedule(schedule)

    def __deal_with_single_schedule(self, cyclic_schedule):
        if self.__check_if_need_to_schedule(cyclic_schedule):
            self.__request_watering(cyclic_schedule)

    def __check_if_need_to_schedule(self, cyclic_schedule):
        barrier = settings.LATENCY_BARRIER
        now = timezone.now()

        if self.__in_latency_barrier(cyclic_schedule.time, barrier):
            count = ScheduledWatering.objects.filter(cyclic_schedule=cyclic_schedule, creation_date__gte=now - barrier,
                                                     creation_date__lte=now).count()
            return count == 0
        else:
            return False

    # todo: opaque in transaction
    def __request_watering(self, cyclic_schedule):
        scheduled_watering = ScheduledWatering.objects.create(cyclic_schedule=cyclic_schedule)
        scheduled_watering.save()
        self.__send_event_to_water_unit(scheduled_watering)

    def __send_event_to_water_unit(self, scheduled_watering):
        message = self.__create_water_unit_message(scheduled_watering)
        self.__channel.basic_publish(exchange='',
                                     routing_key=self.__routing_key,
                                     body=message)
        pass

    @staticmethod
    def __create_water_unit_message(scheduled_watering):
        message_dict = {'watering_id': scheduled_watering.id,
                        'creation_date': scheduled_watering.creation_date.isoformat(),
                        'amount': scheduled_watering.cyclic_schedule.water_amount,
                        'ttl': int(settings.WATERING_MESSAGES_TTL.total_seconds())}
        return json.dumps(message_dict)

    @staticmethod
    def __in_latency_barrier(schedule_time, max_latency):
        now_time = timezone.now().time()
        now_time_in_sec = (datetime.combine(date.min, now_time) - datetime.min).total_seconds()
        schedule_time_in_sec = (datetime.combine(date.min, schedule_time) - datetime.min).total_seconds()
        one_day_sec = timedelta(days=1).total_seconds()

        if (now_time_in_sec - max_latency.total_seconds()) < 0:
            return schedule_time_in_sec >= one_day_sec - (max_latency.total_seconds() - now_time_in_sec)
        else:
            return (schedule_time_in_sec <= now_time_in_sec) and (
                    schedule_time_in_sec >= now_time_in_sec - max_latency.total_seconds())
