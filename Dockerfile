FROM python:3-slim
MAINTAINER "Balhazar Rouberol <br@imap.cc>"

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install .
CMD izk
