FROM python:3.12
WORKDIR /code
RUN apt-get update && apt-get install -y cron
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY flask /code
