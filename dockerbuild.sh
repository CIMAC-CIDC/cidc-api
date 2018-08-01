#!/bin/bash

docker build -t "ingestion-api" .
docker tag ingestion-api gcr.io/cidc-dfci/ingestion-api:latest
docker push gcr.io/cidc-dfci/ingestion-api:latest
