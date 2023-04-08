FROM python:3.8-slim

ENV PORT 8080
ENV FLASK_APP gdsarea

WORKDIR /work
RUN apt-get update \
    && apt-get install -y \
    gcc g++ \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir Flask gunicorn gdspy
COPY ./gdsarea/  /work/gdsarea
WORKDIR /work

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 'gdsarea:create_app()'
