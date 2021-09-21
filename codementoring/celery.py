# Standard Library
import os
import kombu
import json
import time

from celery import Celery, bootsteps
from celery.exceptions import Reject
from django.db import transaction
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codementoring.settings')
app = Celery('codementoring')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def rabbitmq_conn():
    return app.pool.acquire(block=True)


with rabbitmq_conn() as conn:
    queue_codementoring_student = kombu.Queue(
        name='codementoring.students',
        exchange='amq.topic',
        routing_key='saved',
        channel=conn,
        queue_arguments={
        'x-dead-letter-exchange': ''},
        durable=True
    )

    queue_codementoring_student.declare()


class NewStudentConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [
            kombu.Consumer(
                channel,
                queues=[queue_codementoring_student],
                callbacks=[self.handle_message],
                accept=['json']
            )
        ]

    def _process_message(self, data):
        from app.models import Student
        data = json.loads(data)

        Student.objects.update_or_create(
            name=data['name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            active=data['active']
        )

        print("✔️   ==> Student " + data['name'] + " salvo com sucesso!")

        settings.ALLOWED_HOSTS.clear()

    def handle_message(self, data, message):
        try:
            with transaction.atomic():
                self._process_message(data)
        except Exception as e:
            Reject(e, requeue=False)
        message.ack()




app.steps['consumer'].add(NewStudentConsumerStep)
