FROM python:3.6

RUN mkdir /app
COPY ./Pipfile /app
COPY ./Pipfile.lock /app
WORKDIR /app

RUN pip install pipenv && pipenv install --system
RUN pip install gunicorn 

COPY . /app