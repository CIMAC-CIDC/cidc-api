FROM python:3.6

COPY . /app
WORKDIR /app

RUN pip install pipenv && pipenv install --system

CMD ["python", "ingestion_api.py"] 
