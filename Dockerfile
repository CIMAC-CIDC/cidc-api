FROM python:3

COPY . /app
WORKDIR /app

RUN pip install pipenv \
    && pipenv install --system \
    && groupadd -g 999 eve-runner && \
        useradd -r -u 999 -g eve-runner eve-runner

RUN mkdir -p /home/jenkins/workspace && \
    chown -R eve-runner /home/jenkins/workspace
USER eve-runner
CMD ["python", "ingestion_api.py"] 
