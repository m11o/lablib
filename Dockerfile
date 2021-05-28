FROM python:latest

RUN apt-get update
RUN apt-get install -y build-essential wget vim

ENV APP_ROOT /app
RUN mkdir $APP_ROOT
WORKDIR $APP_ROOT

ADD . $APP_ROOT

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt
