FROM python:3.6.5-slim
MAINTAINER "Balhazar Rouberol <br@imap.cc>"

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD izk
