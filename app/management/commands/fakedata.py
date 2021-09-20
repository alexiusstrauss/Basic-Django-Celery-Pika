from django.core.management.base import BaseCommand
from app.models import Pessoa
from faker import Faker


class Command(BaseCommand):
    help = "Criando base de dados de pessoas"

    def add_arguments(self , parser):
        parser.add_argument('--total', action='append', type=int)

    def handle(self, *args, **kwargs):
        fake = Faker()

        total = 1000
        if kwargs['total'] is not None:
            total = int(kwargs['total'][0])

        for _ in range(total):
            email = fake.email()
            if not Pessoa.objects.filter(email=email).count() > 0:
                p           = Pessoa()
                p.name      = fake.first_name()
                p.last_name = fake.last_name()
                p.phone     = fake.msisdn()
                p.email     = email
                p.active    = True
                p.save()
        
        print("✔️  ---> Criado o total de " + str(total) + " registros")