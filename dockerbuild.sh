#!/bin/bash

docker build -t "ingestion-api" .
docker tag ingestion-api undivideddocker/ingestion-api:latest
docker push undivideddocker/ingestion-api:latest
