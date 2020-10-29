FROM python:3.8-slim

RUN apt-get update && apt-get install -y git libjpeg-turbo-progs zlib1g-dev gcc fish vim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Can be overridden by a volume mount.
COPY . /app

RUN pip install -r requirements.txt --src /usr/local/src

# Will output the static files to /app/static.
RUN python manage.py collectstatic --no-input
