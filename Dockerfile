FROM python:3
ENV PYTHONUNBUFFERED 1
COPY demo /demo
WORKDIR /demo
RUN pip install -r requirements.txt && pip install -r requirements-dev.txt