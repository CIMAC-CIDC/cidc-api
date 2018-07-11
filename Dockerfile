FROM python:3.6

COPY . /app
WORKDIR /app

RUN pip install pipenv && pipenv install --system
RUN pip install gunicorn 
