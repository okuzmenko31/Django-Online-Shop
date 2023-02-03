FROM python:3.11

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /rvshop/app

COPY req.txt /rvshop/req.txt
RUN pip install -r /rvshop/req.txt
COPY . .