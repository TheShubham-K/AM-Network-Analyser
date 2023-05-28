FROM python:3.9.2-buster

WORKDIR /usr/src/app

USER root
RUN apt update -y
RUN apt install tcpdump -y
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ./parse.sh