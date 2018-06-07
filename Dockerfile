FROM python:3

COPY . /app
WORKDIR /app

RUN pip install pipenv \
    && pipenv install --system \
    && groupadd -g 999 eve-runner && \
        useradd -r -u 999 -g eve-runner eve-runner

USER eve-runner
CMD ["python", "ingestion_api.py"] 
