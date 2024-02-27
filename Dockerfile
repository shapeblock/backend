FROM python:3.12-slim

RUN apt-get update && apt-get -yqq install git

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /app/

