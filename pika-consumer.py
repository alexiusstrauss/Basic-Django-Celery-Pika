import os, time, pika, django, json
from app.models import Student

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codementoring.settings')
django.setup()

QUEUE = 'codementoring.students'


def save_student(data):
    data = json.loads(data)

    if Student.objects.filter(email=data['email']).exists():
        s = Student.objects.get(email=data['email'])
        s.name = data['name']
        s.last_name = data['last_name']
        s.phone = data['phone']
        s.active = data['active']
    else:
        s = Student(name=data['name'], 
                last_name=data['last_name'], 
                email=data['email'], 
                phone=data['phone'], 
                active=data['active']
        )

    s.save()
    time.sleep(0.09) 
    print("✔️   ==> Student " + s.name + " salvo com sucesso!")


def callback(ch, method, properties, body):
    save_student(body)
    channel.basic_ack(method.delivery_tag)
    

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672, '/', credentials)
    )

channel = connection.channel()
result = channel.queue_declare(
    queue=QUEUE, 
    exclusive=False, 
    durable=True
    )

queue_name = result.method.queue
channel.queue_bind(exchange='amq.topic', queue=queue_name, routing_key='saved')

channel.basic_consume(queue=QUEUE,
                      auto_ack=False,
                      on_message_callback=callback
                      )
					  
                      
print(' [*] Aguardando menssagens na fila ' + QUEUE + '. pressione CTRL+C para sair')

channel.start_consuming()