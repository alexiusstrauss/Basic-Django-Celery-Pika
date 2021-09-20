import os
import pika
import django
import time
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codementoring.settings')
django.setup()

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()


from app.models import Pessoa
pessoas = Pessoa.objects.all()


def get_data_json(Pessoa):
    dados = {
        'name': Pessoa.name,
        'last_name': Pessoa.last_name,
        'email': Pessoa.email,
        'phone': Pessoa.phone,
        'active': True
    }
    return json.dumps(dados)



for pessoa in pessoas:
    channel.basic_publish(exchange='amq.topic',
						  routing_key='saved',
						  body=get_data_json(pessoa))
    print(" ✔️  --> Enviada '" + pessoa.name + "'")

connection.close()