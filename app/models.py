from django.db import models
from app.menssageria import RabbitMQMessager
import json

# Create your models here.
class Student(models.Model):

    class Meta:
        ordering = ['pk']

    name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=False, unique=True)
    phone = models.CharField(max_length=20, blank=False)
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.name


class Pessoa(models.Model):


    name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=False, unique=True)
    phone = models.CharField(max_length=20, blank=False)
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return "%s %s | %s" % (self.name, self.last_name, self.email)

    def get_data_json(self):
        dados = {
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'active': self.active
        }

        return json.dumps(dados)




