FROM python:latest

RUN apt update && apt upgrade -y
RUN apt install python3-pip -y
RUN apt install ffmpeg -y

COPY . /snnot
WORKDIR /snnot

RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

CMD python3 main.py