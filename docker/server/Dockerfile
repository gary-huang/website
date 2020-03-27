FROM python:3.8-slim

RUN apt-get update && apt-get install -y git libjpeg-turbo-progs zlib1g-dev gcc fish

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY ./requirements.txt /code

RUN pip install -r requirements.txt --src /usr/local/src
