FROM python:3.12


RUN apt-get update -y
RUN apt-get upgrade -y


WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
