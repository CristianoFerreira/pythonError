FROM python:latest
MAINTAINER dev@example.com

RUN apt-get update
RUN apt-get install curl vim -y

ADD requirements.txt /app/requirements.txt
ADD . /app

cd /app
RUN pip install -r requirements.txt

RUN chmod 777 -R /app

ENV DEBUG true
EXPOSE 5005

CMD uvicorn app.main:app --host 0.0.0.0 --port 5005
