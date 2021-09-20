FROM rabbitmq:3.9-management-alpine

COPY rabbitmq.config /etc/rabbitmq/
RUN chmod 777 /etc/rabbitmq/rabbitmq.config

WORKDIR /var/lib/rabbitmq/
RUN rabbitmq-plugins enable rabbitmq_management  --offline
RUN rabbitmq-plugins list


# pull official base image
FROM python:3.9.7-slim

ENV MICRO_SERVICE=/home/app/microservice

# set work directory
RUN mkdir -p $MICRO_SERVICE
RUN mkdir -p $MICRO_SERVICE/static

# where the code lives
WORKDIR $MICRO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update 
RUN pip install --upgrade pip
RUN apt-get -y install libpq-dev gcc

# copy project
COPY . $MICRO_SERVICE

# install dependencies
RUN pip install -r requirements.txt