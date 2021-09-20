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
        routing_key='model.student.saved',
        channel=conn,
        durable=True
    )

    # declarando parametros do consumidor
    queue_codementoring_student.declare()


class NewStudentConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        data = [
            kombu.Consumer(
                channel,
                queues=[queue_codementoring_student],
                callbacks=[self.handle_message],
                accept=['json']
            )
        ]
        return data

    def handle_message(self, data, message):
        try:
            with transaction.atomic():
                #from app.models import Student
                data = json.loads(data)
                time.sleep(1)
                print("✔️   ==> Student " +
                      data['name'] + " salvo com sucesso!")
                settings.ALLOWED_HOSTS.clear()
        except Exception as e:
            Reject(e, requeue=False)
        message.ack()


app.steps['consumer'].add(NewStudentConsumerStep)
