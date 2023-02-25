FROM python:3.11

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /shop/app

COPY req.txt /shop/req.txt
RUN pip install -r /shop/req.txt
COPY . .
