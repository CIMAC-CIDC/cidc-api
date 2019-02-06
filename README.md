| Branch | Coverage | Code Quality |
| --- | --- | --- |
| Master | [![codecov](https://codecov.io/gh/CIMAC-CIDC/cidc-api/branch/master/graph/badge.svg)](https://codecov.io/gh/CIMAC-CIDC/cidc-api/branch/master/) | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6c9f0537475f46afa84f68923dd5f421)](https://www.codacy.com/app/CIMAC-CIDC/cidc-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CIMAC-CIDC/cidc-api&amp;utm_campaign=Badge_Grade?branch=master)
| Staging | [![codecov](https://codecov.io/gh/CIMAC-CIDC/cidc-api/branch/staging/graph/badge.svg)](https://codecov.io/gh/CIMAC-CIDC/cidc-api/branch/staging/) | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6c9f0537475f46afa84f68923dd5f421)](https://www.codacy.com/app/CIMAC-CIDC/cidc-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CIMAC-CIDC/cidc-api&amp;utm_campaign=Badge_Grade?branch=staging)

## CIDC-API
This is the API that powers the CIDC project. It interacts with a MongoDB and controlls both user uploads of data, and user requests for data. This is designed primarily to be run as a helm chart on kubernetes, but can also be run as a docker image.

### Build
To build the Docker image, simply run the `Dockerfile` in the root of the repository.

## Installation
This application is not meant to be run outside of the context of a container such as Docker, Docker-Compose, or Kubernetes. The easiest way to install this application without building it yourself is to copy the Helm chart from our [helm repo](https://github.com/CIMAC-CIDC/cidc-devops/tree/master/kubernetes/helm/ingestion-api). And then use `helm install` to install the service on your kubernetes cluster.

#### Running Tests

To run unit tests: 

    pipenv shell
    pytest

To generate an XML for code coverage plugins:

    pipenv shell
    pytest --cov-report xml:coverage.xml --cov ./

To generate an HTML output:
    
    pipenv shell
    pytest --html=report.html