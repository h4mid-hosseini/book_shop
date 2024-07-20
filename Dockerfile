FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ Asia/Tehran
RUN apt-get update && \
    apt-get install tzdata 

RUN mkdir /home/backend
WORKDIR /home/backend


COPY backend/requirements.txt /home/backend/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /home/

